from PyQt5.QtCore import Qt, QCoreApplication

from src.ui.ui_handling import move_slider, show_bar_time

STEP = 10


def move_slider_left(main_app):
    try:
        move_slider(main_app.df, main_app.fig, main_app.ax, main_app.slider, main_app.bars_to_display,
                    main_app.selector_var, main_app.selector_info, -STEP)
        show_bar_time(main_app.df, main_app.slider, main_app.time_info_label)
        return 0  # Aucune erreur
    except Exception as e:
        print(f"Erreur lors du déplacement du curseur vers la gauche : {e}")
        return -1  # Code d'erreur


def move_slider_right(main_app):
    try:
        move_slider(main_app.df, main_app.fig, main_app.ax, main_app.slider, main_app.bars_to_display,
                    main_app.selector_var, main_app.selector_info, STEP)
        show_bar_time(main_app.df, main_app.slider, main_app.time_info_label)
        return 0  # Aucune erreur
    except Exception as e:
        print(f"Erreur lors du déplacement du curseur vers la droite : {e}")
        return -1  # Code d'erreur


def key_press_event(main_app, event):
    try:
        if STEP == 1:
            if event.key() == Qt.Key_Left:
                for _ in range(STEP):
                    main_app.slider.triggerAction(main_app.slider.SliderSingleStepSub)
                    QCoreApplication.processEvents()
            elif event.key() == Qt.Key_Right:
                for _ in range(STEP):
                    main_app.slider.triggerAction(main_app.slider.SliderSingleStepAdd)
                    QCoreApplication.processEvents()
        else:
            if event.key() == Qt.Key_Left:
                main_app.slider.setValue(main_app.slider.value() - STEP)
                main_app.slider.triggerAction(main_app.slider.SliderSingleStepSub)
            elif event.key() == Qt.Key_Right:
                main_app.slider.setValue(main_app.slider.value() + STEP)
                main_app.slider.triggerAction(main_app.slider.SliderSingleStepAdd)
        return 0  # Aucune erreur
    except Exception as e:
        print(f"Erreur lors de l'événement de pression de touche : {e}")
        return -1  # Code d'erreur
