# SPDX-FileCopyrightText: 2026 LichtFeld Studio Authors
# SPDX-License-Identifier: GPL-3.0-or-later
"""Regression checks for retained RmlUI menu bar resources."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_menubar_submenus_are_stacked_above_overlay_and_hit_testable():
    rcss = (
        PROJECT_ROOT
        / "src"
        / "visualizer"
        / "gui"
        / "rmlui"
        / "resources"
        / "menubar.rcss"
    ).read_text(encoding="utf-8")

    assert "#dropdown-overlay" in rcss
    assert "#dropdown-container" in rcss
    assert ".submenu-popup" in rcss
    assert "z-index: 1;" in rcss
    assert "z-index: 2;" in rcss
    assert "z-index: 3;" in rcss
    assert "#dropdown-container {\n    display: none;\n    position: absolute;\n    overflow: visible;" in rcss
    assert ".dropdown-popup" in rcss and "overflow: visible;" in rcss
    assert ".submenu-popup:hover" in rcss
    assert "pointer-events: auto;" in rcss


def test_rml_tooltips_request_only_pending_animation_frames():
    tooltip_header = (
        PROJECT_ROOT
        / "src"
        / "visualizer"
        / "gui"
        / "rmlui"
        / "rml_tooltip.hpp"
    ).read_text(encoding="utf-8")
    viewport_header = (
        PROJECT_ROOT
        / "src"
        / "visualizer"
        / "gui"
        / "rml_viewport_overlay.hpp"
    ).read_text(encoding="utf-8")
    viewport_cpp = (
        PROJECT_ROOT
        / "src"
        / "visualizer"
        / "gui"
        / "rml_viewport_overlay.cpp"
    ).read_text(encoding="utf-8")
    gui_manager_cpp = (
        PROJECT_ROOT
        / "src"
        / "visualizer"
        / "gui"
        / "gui_manager.cpp"
    ).read_text(encoding="utf-8")

    assert "bool needsFrame() const" in tooltip_header
    assert "&& !visible_" in tooltip_header
    assert "tooltip_.needsFrame()" in viewport_header
    assert "tooltip_.hasActiveState() && applyFrameTooltip()" in viewport_cpp
    assert "setContextNeedsPassiveMouseMoveFrames(rml_context_, tooltip_.needsFrame())" in viewport_cpp
    assert "rml_viewport_overlay_.needsAnimationFrame()" in gui_manager_cpp
