from check_one import *
from check_two import *
from check_three import *
from user_gui import *


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(check_one_=pressure_check, check_two_=gazi_check, check_three_=three)
    window.show()
    sys.exit(app.exec_())