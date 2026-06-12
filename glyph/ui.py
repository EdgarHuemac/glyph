import curses
import curses.ascii
import threading
import time
from . import algorithms as alg_registry

# ── color pair IDs ────────────────────────────────────────────────────────────
CP_TITLE    = 1   # header bar
CP_STATUS   = 2   # status / footer bar
CP_INPUT    = 3   # input box border + label
CP_ROW_ALT  = 4   # alternating row background
CP_ROW_SEL  = 5   # selected/highlighted row
CP_LABEL    = 6   # algorithm name
CP_VALUE    = 7   # result value
CP_CAT      = 8   # category badge
CP_ERR      = 9   # error text
CP_BORDER   = 10  # panel borders
CP_CURSOR   = 11  # cursor indicator


def _init_colors():
    curses.start_color()
    curses.use_default_colors()
    # Dark background palette
    curses.init_pair(CP_TITLE,   curses.COLOR_BLACK,  curses.COLOR_CYAN)
    curses.init_pair(CP_STATUS,  curses.COLOR_BLACK,  curses.COLOR_BLUE)
    curses.init_pair(CP_INPUT,   curses.COLOR_CYAN,   -1)
    curses.init_pair(CP_ROW_ALT, curses.COLOR_WHITE,  -1)
    curses.init_pair(CP_ROW_SEL, curses.COLOR_BLACK,  curses.COLOR_GREEN)
    curses.init_pair(CP_LABEL,   curses.COLOR_CYAN,   -1)
    curses.init_pair(CP_VALUE,   curses.COLOR_WHITE,  -1)
    curses.init_pair(CP_CAT,     curses.COLOR_YELLOW, -1)
    curses.init_pair(CP_ERR,     curses.COLOR_RED,    -1)
    curses.init_pair(CP_BORDER,  curses.COLOR_BLUE,   -1)
    curses.init_pair(CP_CURSOR,  curses.COLOR_BLACK,  curses.COLOR_WHITE)


CATEGORY_ABBREV = {
    "binary_text":  "BIN",
    "web_escape":   "WEB",
    "ciphers":      "CPH",
    "numbers":      "NUM",
    "unicode_repr": "UNI",
    "unicode_norm": "NRM",
    "text_case":    "TXT",
    "text_utils":   "UTL",
    "dates":        "DTE",
    "colors":       "CLR",
    "hashes":       "HSH",
}


class GlyphUI:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config
        self.input_buf = ""
        self.cursor_pos = 0
        self.scroll_offset = 0
        self.selected_row = 0
        self.results = []          # list of (algo, result_str)
        self._compute_lock = threading.Lock()
        self._pending = False

    # ── layout helpers ────────────────────────────────────────────────────────

    def _dimensions(self):
        h, w = self.stdscr.getmaxyx()
        # Reserve: 1 title + 4 input + 1 separator + rest results + 1 footer
        input_h   = 4
        title_h   = 1
        footer_h  = 1
        results_h = max(3, h - title_h - input_h - 1 - footer_h)
        return h, w, title_h, input_h, results_h, footer_h

    # ── drawing ───────────────────────────────────────────────────────────────

    def _draw_title(self, w):
        title = "  ◈ GLYPH — Encoding & Decoding Swiss Knife "
        mode_tag = ""
        if self.config.mode:
            mode_tag = f" [{self.config.mode.upper()}] "
        if self.config.category:
            mode_tag += f"[{self.config.category}] "
        bar = title + mode_tag
        bar = bar.ljust(w)[:w]
        try:
            self.stdscr.addstr(0, 0, bar, curses.color_pair(CP_TITLE) | curses.A_BOLD)
        except curses.error:
            pass

    def _draw_input(self, y, w):
        h_box = 3
        # border
        box_w = min(w - 2, 120)
        x0 = 1
        try:
            self.stdscr.attron(curses.color_pair(CP_BORDER))
            self.stdscr.addstr(y,     x0, "┌" + "─" * (box_w - 2) + "┐")
            self.stdscr.addstr(y + 1, x0, "│" + " " * (box_w - 2) + "│")
            self.stdscr.addstr(y + 2, x0, "└" + "─" * (box_w - 2) + "┘")
            self.stdscr.attroff(curses.color_pair(CP_BORDER))

            label = " INPUT ▶ "
            self.stdscr.addstr(y, x0 + 2, label, curses.color_pair(CP_INPUT) | curses.A_BOLD)

            inner_w = box_w - 4
            disp = self.input_buf
            # scroll input text horizontally if too long
            if self.cursor_pos >= inner_w:
                start = self.cursor_pos - inner_w + 1
                disp = disp[start:]
                cur_x = inner_w
            else:
                cur_x = self.cursor_pos

            disp_clipped = disp[:inner_w].ljust(inner_w)
            self.stdscr.addstr(y + 1, x0 + 2, disp_clipped, curses.color_pair(CP_VALUE))

            # draw cursor
            cur_char = (disp_clipped[cur_x] if cur_x < len(disp_clipped) else " ")
            self.stdscr.addstr(y + 1, x0 + 2 + cur_x, cur_char,
                               curses.color_pair(CP_CURSOR) | curses.A_BLINK)
        except curses.error:
            pass

    def _draw_separator(self, y, w):
        label = "─── Results " + ("─" * max(0, w - 14))
        try:
            self.stdscr.addstr(y, 0, label[:w], curses.color_pair(CP_BORDER))
        except curses.error:
            pass

    def _draw_results(self, y_start, max_rows, w):
        if not self.results:
            msg = "  Type something above to see results…"
            try:
                self.stdscr.addstr(y_start, 0, msg[:w], curses.color_pair(CP_CAT))
            except curses.error:
                pass
            return

        visible = self.results[self.scroll_offset: self.scroll_offset + max_rows]
        for i, (algo, result) in enumerate(visible):
            y = y_start + i
            abs_idx = self.scroll_offset + i
            is_selected = (abs_idx == self.selected_row)

            cat_abbrev = CATEGORY_ABBREV.get(algo.category, algo.category[:3].upper())
            cat_badge  = f"[{cat_abbrev}]"
            name_col   = f" {algo.name:<28}"
            sep        = " │ "
            val_start  = 1 + len(cat_badge) + 1 + len(name_col) + len(sep)
            val_w      = max(10, w - val_start - 1)

            result_line = str(result).replace("\n", "↵").replace("\t", "→")
            result_clip = result_line[:val_w]

            attr_row  = curses.color_pair(CP_ROW_SEL) if is_selected else (
                        curses.color_pair(CP_ROW_ALT) if abs_idx % 2 == 0 else 0)

            try:
                self.stdscr.addstr(y, 0, " " * w, attr_row)
                # category badge
                self.stdscr.addstr(y, 1, cat_badge,
                                   curses.color_pair(CP_CAT) | (curses.A_REVERSE if is_selected else 0))
                # algorithm name
                self.stdscr.addstr(y, 1 + len(cat_badge) + 1, name_col,
                                   curses.color_pair(CP_LABEL) | (curses.A_BOLD if is_selected else 0))
                # separator
                self.stdscr.addstr(y, 1 + len(cat_badge) + 1 + len(name_col), sep,
                                   curses.color_pair(CP_BORDER))
                # result
                is_err = result_clip.startswith("[error")
                r_attr = curses.color_pair(CP_ERR) if is_err else curses.color_pair(CP_VALUE)
                self.stdscr.addstr(y, val_start, result_clip, r_attr)
            except curses.error:
                pass

    def _draw_footer(self, y, w, total):
        shown_end = min(self.scroll_offset + 100, total)
        info = (f"  ↑↓ Navigate  Ctrl+C Quit  "
                f"│ {self.scroll_offset+1}-{shown_end}/{total} results  "
                f"│ Ctrl+U Clear  │ Enter Copy selected")
        bar = info.ljust(w)[:w]
        try:
            self.stdscr.addstr(y, 0, bar, curses.color_pair(CP_STATUS))
        except curses.error:
            pass

    def draw(self):
        self.stdscr.erase()
        h, w, title_h, input_h, results_h, footer_h = self._dimensions()
        self._draw_title(w)
        self._draw_input(title_h, w)
        sep_y = title_h + input_h
        self._draw_separator(sep_y, w)
        self._draw_results(sep_y + 1, results_h, w)
        footer_y = h - footer_h
        self._draw_footer(footer_y, w, len(self.results))
        self.stdscr.refresh()

    # ── compute ───────────────────────────────────────────────────────────────

    def _compute_results(self):
        algos = alg_registry.get_all(
            mode=self.config.mode,
            category=self.config.category,
            exclude=self.config.exclude,
        )
        new_results = []
        text = self.input_buf
        for algo in algos:
            result = algo.safe_process(text)
            new_results.append((algo, result))
        with self._compute_lock:
            self.results = new_results
            # clamp selection
            if self.selected_row >= len(self.results):
                self.selected_row = max(0, len(self.results) - 1)

    def _async_compute(self):
        self._pending = True
        t = threading.Thread(target=self._compute_results, daemon=True)
        t.start()

    # ── input handling ────────────────────────────────────────────────────────

    def handle_key(self, key):
        h, w, title_h, input_h, results_h, footer_h = self._dimensions()

        if key == curses.KEY_UP:
            if self.selected_row > 0:
                self.selected_row -= 1
                if self.selected_row < self.scroll_offset:
                    self.scroll_offset = self.selected_row
        elif key == curses.KEY_DOWN:
            if self.selected_row < len(self.results) - 1:
                self.selected_row += 1
                if self.selected_row >= self.scroll_offset + results_h:
                    self.scroll_offset = self.selected_row - results_h + 1
        elif key == curses.KEY_PPAGE:  # Page Up
            self.selected_row = max(0, self.selected_row - results_h)
            self.scroll_offset = max(0, self.scroll_offset - results_h)
        elif key == curses.KEY_NPAGE:  # Page Down
            self.selected_row = min(len(self.results)-1, self.selected_row + results_h)
            if self.selected_row >= self.scroll_offset + results_h:
                self.scroll_offset = self.selected_row - results_h + 1
        elif key == curses.KEY_HOME:
            self.cursor_pos = 0
        elif key == curses.KEY_END:
            self.cursor_pos = len(self.input_buf)
        elif key == curses.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key == curses.KEY_RIGHT:
            if self.cursor_pos < len(self.input_buf):
                self.cursor_pos += 1
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if self.cursor_pos > 0:
                self.input_buf = self.input_buf[:self.cursor_pos-1] + self.input_buf[self.cursor_pos:]
                self.cursor_pos -= 1
                self._async_compute()
        elif key == curses.KEY_DC:  # Delete
            if self.cursor_pos < len(self.input_buf):
                self.input_buf = self.input_buf[:self.cursor_pos] + self.input_buf[self.cursor_pos+1:]
                self._async_compute()
        elif key == 21:  # Ctrl+U — clear
            self.input_buf = ""
            self.cursor_pos = 0
            self._async_compute()
        elif key == 10 or key == curses.KEY_ENTER:  # Enter — copy selected
            if self.results:
                _, result = self.results[self.selected_row]
                self.input_buf = str(result).replace("↵", "\n")
                self.cursor_pos = len(self.input_buf)
                self._async_compute()
        elif 32 <= key <= 126:  # printable ASCII
            self.input_buf = self.input_buf[:self.cursor_pos] + chr(key) + self.input_buf[self.cursor_pos:]
            self.cursor_pos += 1
            self._async_compute()
        elif key >= 128:  # Handle wide/unicode input from curses
            try:
                ch = chr(key)
                self.input_buf = self.input_buf[:self.cursor_pos] + ch + self.input_buf[self.cursor_pos:]
                self.cursor_pos += 1
                self._async_compute()
            except (ValueError, OverflowError):
                pass

    # ── main loop ─────────────────────────────────────────────────────────────

    def run(self):
        _init_colors()
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        self._async_compute()

        while True:
            self.draw()
            key = self.stdscr.getch()
            if key == 3:   # Ctrl+C
                break
            if key == -1:
                time.sleep(0.016)  # ~60fps idle
                continue
            self.handle_key(key)
