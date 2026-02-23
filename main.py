import dataclasses
import typing

import glfw
import numpy as np
from slimgui import imgui
import slimgui.integrations.glfw as imgui_glfw
from OpenGL import GL

from lib.algorithm_manager import AlgorithmManager
from lib.grid import Grid

TITLE_FONT_SIZE: float = 32.0
HEADER_FONT_SIZE: float = 24.0
NORMAL_FONT_SIZE: float = 18.0
HINT_FONT_SIZE: float = 12.0

MAX_GRID_HEIGHT: int = 512
MIN_GRID_HEIGHT: int = 32

MAX_GRID_WIDTH: int = 512
MIN_GRID_WIDTH: int = 32

EXPLORED_COLOR: tuple[int, int, int, int] = (0, 255, 0, 255)
FRONTIER_COLOR: tuple[int, int, int, int] = (0, 255, 0, 255)
PATH_COLOR: tuple[int, int, int, int] = (0, 0, 255, 255)

FREE_COLOR: tuple[int, int, int, int] = (255, 255, 255, 255)
WALL_COLOR: tuple[int, int, int, int] = (62, 61, 83, 255)

COLOR_LUT = np.array(
    [
        FREE_COLOR,
        WALL_COLOR,
    ],
    dtype=np.uint8,
)


@dataclasses.dataclass(slots=True)
class State:
    grid_height: int = MIN_GRID_HEIGHT
    grid_width: int = MIN_GRID_WIDTH
    seed: str | None = None
    texture_height: int = MIN_GRID_HEIGHT
    texture_width: int = MIN_GRID_WIDTH

    menu_visible: bool = True
    started: bool = False


class App:
    __slots__: tuple[str, ...] = (
        "algorithm_manager",
        "context",
        "grid_texture",
        "renderer",
        "state",
    )

    algorithm_manager: AlgorithmManager
    context: imgui.WrappedContext
    grid_texture: int | None
    renderer: imgui_glfw.GlfwRenderer
    state: State

    def __init__(self):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        window = glfw.create_window(640, 320, "Wegsuche", None, None)
        if not window:
            glfw.terminate()
            raise RuntimeError("Failed to create window")

        glfw.make_context_current(window)

        self.context = imgui.create_context()
        self.renderer = imgui_glfw.GlfwRenderer(
            window, prev_key_callback=self.prev_key_callback
        )

        self.grid_texture = None

        self.algorithm_manager = AlgorithmManager()
        self.state = State()

    def prev_key_callback(self, _window, key: int, _scan, action: int, _mods):
        if action == glfw.PRESS and key == glfw.KEY_ESCAPE:
            self.state.menu_visible = True
            self.state.started = False

    def render_grid(self, fb_h: int, fb_w: int):
        assert self.grid_texture is not None

        grid_aspect = self.state.grid_width / self.state.grid_height

        if grid_aspect > 1:
            draw_h = fb_w / grid_aspect
            draw_w = fb_w
            offset_x = 0
            offset_y = (fb_h - draw_h) / 2
        elif grid_aspect < 1:
            draw_h = fb_h
            draw_w = fb_h * grid_aspect
            offset_x = (fb_w - draw_w) / 2
            offset_y = 0
        else:
            draw_h = fb_h
            draw_w = fb_w
            offset_x = 0
            offset_y = 0

        imgui.set_next_window_pos((0.0, 0.0))
        imgui.set_next_window_size((fb_w, fb_h))

        flags = (
            imgui.WindowFlags.NO_COLLAPSE
            | imgui.WindowFlags.NO_MOVE
            | imgui.WindowFlags.NO_NAV_FOCUS
            | imgui.WindowFlags.NO_RESIZE
            | imgui.WindowFlags.NO_SAVED_SETTINGS
            | imgui.WindowFlags.NO_TITLE_BAR
        )

        _ = imgui.begin("##grid", flags=flags)
        imgui.set_cursor_pos((offset_x, offset_y))

        imgui.image(
            self.grid_texture,
            (draw_w, draw_h),
        )

        if self.state.started != True and self.algorithm_manager.algorithm_instance.path is None:
            draw_list = imgui.get_window_draw_list()
            imgui.push_font(None, HEADER_FONT_SIZE)

            text = "No Solution"
            text_w, text_h = imgui.calc_text_size(text)

            banner_x = offset_x
            banner_w = draw_w

            banner_h = text_h * 3.2
            banner_y = offset_y + (draw_h - banner_h) * 0.5

            text_x = banner_x + (banner_w - text_w) * 0.5
            text_y = banner_y + (banner_h - text_h) * 0.5

            draw_list.add_rect_filled(
                (banner_x, banner_y),
                (banner_x + banner_w, banner_y + banner_h),
                imgui.get_color_u32((0, 0, 0, 0.75)),
            )

            draw_list.add_text(
                (text_x, text_y),
                imgui.get_color_u32((1, 1, 1, 1)),
                text,
            )

            imgui.pop_font()

        imgui.end()

    def render_menu(self, fb_h: int, fb_w: int):
        imgui.set_next_window_pos((0.0, 0.0))
        imgui.set_next_window_size((fb_w, fb_h))

        flags = (
            imgui.WindowFlags.NO_COLLAPSE
            | imgui.WindowFlags.NO_MOVE
            | imgui.WindowFlags.NO_NAV_FOCUS
            | imgui.WindowFlags.NO_RESIZE
            | imgui.WindowFlags.NO_SAVED_SETTINGS
        )

        imgui.push_font(None, NORMAL_FONT_SIZE)

        imgui.push_font(None, TITLE_FONT_SIZE)
        _ = imgui.begin("Menu", flags=flags)
        imgui.pop_font()

        imgui.push_font(None, HEADER_FONT_SIZE)
        imgui.separator_text("Algorithm")
        imgui.pop_font()
        imgui.spacing()
        imgui.indent(32.0)

        self.algorithm_manager.render()

        imgui.unindent(32.0)
        imgui.spacing()
        imgui.spacing()

        imgui.push_font(None, HEADER_FONT_SIZE)
        imgui.separator_text("Grid")
        imgui.pop_font()
        imgui.spacing()
        imgui.indent(32.0)

        imgui.text("Height")
        imgui.same_line()
        imgui.push_item_width(128)
        height_changed, new_height = imgui.input_int(
            "##grid_height", self.state.grid_height
        )
        imgui.pop_item_width()
        imgui.same_line()
        imgui.text("Width")
        imgui.same_line()
        imgui.push_item_width(128)
        width_changed, new_width = imgui.input_int(
            "##grid_width", self.state.grid_width
        )
        imgui.pop_item_width()

        imgui.spacing()
        imgui.spacing()

        imgui.text("Seed")

        indent = imgui.get_item_rect_size()[0] + 12
        width = imgui.calc_text_size("Leave blank to generate randomly")[0] * (
            HINT_FONT_SIZE / NORMAL_FONT_SIZE
        )

        imgui.same_line()
        imgui.push_item_width(width)
        seed_changed, new_seed = imgui.input_text("##seed", self.state.seed or "")
        imgui.indent(indent)
        imgui.push_font(None, HINT_FONT_SIZE)
        imgui.text_disabled("Leave blank to generate randomly")
        imgui.unindent(indent)
        imgui.pop_font()

        imgui.spacing()
        imgui.unindent(32.0)
        imgui.pop_font()

        imgui.dummy((0.0, 24.0))

        imgui.push_style_var(imgui.StyleVar.FRAME_ROUNDING, 12.0)
        imgui.push_style_var(imgui.StyleVar.FRAME_PADDING, (16, 10))
        imgui.push_style_color(imgui.Col.BUTTON, (0.01, 0.75, 0.29, 1.0))  # #03C04A
        imgui.push_style_color(
            imgui.Col.BUTTON_HOVERED, (0.18, 0.85, 0.45, 1.0)
        )  # hover
        imgui.push_style_color(
            imgui.Col.BUTTON_ACTIVE, (0.01, 0.59, 0.23, 1.0)
        )  # active
        imgui.push_font(None, HEADER_FONT_SIZE)

        start_btn_label = "Start"
        text_w, _ = imgui.calc_text_size(start_btn_label)
        padding = imgui.get_style().frame_padding[0] * 2
        button_width = text_w + padding

        avail = imgui.get_content_region_avail()[0]
        imgui.set_cursor_pos_x((avail - button_width) * 0.5)

        start_btn_pressed = imgui.button(start_btn_label, (text_w + 2 * 16, 48.0))

        imgui.pop_style_color(3)
        imgui.pop_style_var(2)
        imgui.pop_font()

        if height_changed:
            self.state.grid_height = max(
                min(new_height, MAX_GRID_HEIGHT), MIN_GRID_HEIGHT
            )

        if width_changed:
            self.state.grid_width = max(min(new_width, MAX_GRID_WIDTH), MIN_GRID_WIDTH)

        if seed_changed:
            self.state.seed = new_seed or None

        if start_btn_pressed:
            root = 0
            target = self.state.grid_height * self.state.grid_width - 1

            if self.state.seed is None:
                self.state.seed = str(
                    np.random.default_rng().integers(0, 2**32, dtype=np.uint32)
                )

            grid = Grid.generate(
                self.state.grid_height,
                self.state.grid_width,
                root,
                target,
                np.random.default_rng(
                    np.random.SeedSequence(list(self.state.seed.encode("utf-8")))
                ),
            )

            self.algorithm_manager.instantiate_algorithm(grid, root, target)
            self.update_grid_texture()

            self.state.started = True
            self.state.menu_visible = False

        imgui.end()

    def run(self) -> typing.Never:
        while not glfw.window_should_close(self.renderer.window):
            glfw.poll_events()

            fb_w, fb_h = glfw.get_framebuffer_size(self.renderer.window)

            io = imgui.get_io()
            io.display_size = (fb_w, fb_h)
            GL.glViewport(0, 0, fb_w, fb_h)
            GL.glClear(int(GL.GL_COLOR_BUFFER_BIT) | int(GL.GL_DEPTH_BUFFER_BIT))

            self.renderer.new_frame()
            imgui.new_frame()

            if self.state.menu_visible:
                self.render_menu(fb_h, fb_w)
            else:
                self.render_grid(fb_h, fb_w)

            if self.state.started:
                assert self.algorithm_manager.algorithm_instance is not None

                solution_found = self.algorithm_manager.algorithm_instance.step()

                if solution_found is not None:
                    if solution_found:
                        self.algorithm_manager.algorithm_instance.construct_path()
                    self.state.started = False
                self.update_grid_texture()

            imgui.render()
            self.renderer.render(imgui.get_draw_data())

            glfw.swap_buffers(self.renderer.window)

        self.renderer.shutdown()
        imgui.destroy_context(self.context)
        glfw.terminate()
        exit(0)

    def update_grid_texture(self):
        assert self.algorithm_manager.algorithm_instance is not None

        if (
            self.state.grid_height != self.state.texture_height
            or self.state.grid_width != self.state.texture_width
        ) and self.grid_texture is not None:
            GL.glDeleteTextures([self.grid_texture])

            self.grid_texture = None
            self.state.texture_height = self.state.grid_height
            self.state.texture_width = self.state.grid_width

        if self.grid_texture is None:
            self.grid_texture = GL.glGenTextures(1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.grid_texture)

            GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)

            GL.glTexImage2D(
                GL.GL_TEXTURE_2D,
                0,
                GL.GL_RGBA8,
                self.state.texture_width,
                self.state.texture_height,
                0,
                GL.GL_RGBA,
                GL.GL_UNSIGNED_BYTE,
                None,
            )

            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST
            )
            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST
            )

            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE
            )
            GL.glTexParameteri(
                GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE
            )

            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        rgba = COLOR_LUT[self.algorithm_manager.algorithm_instance.grid.cells]
        flat_view = rgba.reshape(-1, 4)

        flat_view[self.algorithm_manager.algorithm_instance.explored()] = [
            255,
            0,
            0,
            255,
        ]
        flat_view[self.algorithm_manager.algorithm_instance.frontier()] = [
            0,
            255,
            0,
            255,
        ]

        if self.algorithm_manager.algorithm_instance.path is not None:
            flat_view[self.algorithm_manager.algorithm_instance.path] = [0, 0, 255, 255]

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.grid_texture)

        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)

        GL.glTexSubImage2D(
            GL.GL_TEXTURE_2D,
            0,
            0,
            0,
            self.state.texture_width,
            self.state.texture_height,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            rgba,
        )

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


if __name__ == "__main__":
    App().run()
