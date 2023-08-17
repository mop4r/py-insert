import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit

class InsertGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.empresa_label = QLabel("Empresa:")
        self.pcp001_label = QLabel("PCP001 (Código da CCP):")
        self.pcp002_label = QLabel("PCP002 (Número de parcelas):")

        self.empresa_input = QLineEdit()
        self.pcp001_input = QLineEdit()
        self.pcp002_input = QLineEdit()

        self.generate_button = QPushButton("Gerar INSERTS")
        self.generate_button.clicked.connect(self.generate_inserts)

        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText("Os INSERTS gerados serão exibidos aqui...")

        self.copy_button = QPushButton("Copiar")
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        layout = QVBoxLayout()
        layout.addWidget(self.empresa_label)
        layout.addWidget(self.empresa_input)
        layout.addWidget(self.pcp001_label)
        layout.addWidget(self.pcp001_input)
        layout.addWidget(self.pcp002_label)
        layout.addWidget(self.pcp002_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_text)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setWindowTitle("Gerador de INSERTS")
        self.show()

    def generate_inserts(self):
        empresa = self.empresa_input.text()
        pcp001 = self.pcp001_input.text()
        pcp002 = self.pcp002_input.text()

        try:
            empresa = int(empresa)
            pcp001 = int(pcp001)
            pcp002 = int(pcp002)

            pcp003 = 30
            total_days = pcp003 * pcp002

            # Calcular o valor de PCP004 para que a soma de todas as parcelas seja 100
            pcp004 = round(100 / pcp002, 4)

            inserts = ""
            for i in range(1, pcp002 + 1):
                if i == pcp002:
                    # Ajustar o último valor para fechar em 100
                    pcp004_last = round(100 - pcp004 * (pcp002 - 1), 4)
                else:
                    pcp004_last = pcp004

                insert = f'INSERT INTO "DBA"."GES_024" ("EMPRESA","PCP001","PCP002","PCP003","PCP004","PCP005") VALUES({empresa},{pcp001},{i},{pcp003},{pcp004_last},0);\n'
                inserts += insert

                pcp003 += 30  # Incremento de 30 dias em PCP003

            self.result_text.setPlainText(inserts)

        except ValueError:
            self.result_text.setPlainText("Valores inválidos. Certifique-se de que os campos estejam preenchidos corretamente.")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InsertGenerator()
    sys.exit(app.exec_())
