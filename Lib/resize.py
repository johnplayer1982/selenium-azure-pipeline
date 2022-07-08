def resizeMobile(driver):
    driver.set_window_size(450, 800)
    print(' > Resized to mobile')

def resizeTablet(driver):
    driver.set_window_size(1007, 900)
    print(' > Resized to tablet')

def resizeDesktop(driver):
    driver.maximize_window()
    print(' > Maximised window')
