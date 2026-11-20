import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

ARCHIVO_CUENTAS = "cuentas_banco.json"
ARCHIVO_TRANSACCIONES = "transacciones.json"

# ========== FUNCIONES DE DATOS ==========
def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar_transaccion(num_cuenta, tipo, monto, destino=None):
    transacciones = cargar_datos(ARCHIVO_TRANSACCIONES)
    nueva = {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cuenta": num_cuenta,
        "tipo": tipo,
        "monto": monto,
        "destino": destino
    }
    transacciones.append(nueva)
    guardar_datos(ARCHIVO_TRANSACCIONES, transacciones)

# ========== VENTANA PRINCIPAL ==========
class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco en Linea")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        self.cuenta_actual = None
        
        self.pantalla_inicio()
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def pantalla_inicio(self):
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="BANCO EN LINEA", font=("Arial", 24, "bold"), fg="#0a2342").pack(pady=80)
        tk.Label(self.root, text="Su dinero, siempre seguro", font=("Arial", 12), fg="#555").pack(pady=5)
        
        tk.Button(self.root, text="Crear Cuenta Nueva", font=("Arial", 14), bg="#4ecdc4", fg="#0a2342",
                  width=25, height=2, command=self.pantalla_crear_cuenta).pack(pady=30)
        
        tk.Button(self.root, text="Iniciar Sesion", font=("Arial", 14), bg="#0a2342", fg="white",
                  width=25, height=2, command=self.pantalla_iniciar_sesion).pack(pady=10)
        
        tk.Button(self.root, text="Salir", font=("Arial", 12), bg="#e74c3c", fg="white",
                  width=15, command=self.root.quit).pack(pady=40)
    
    def pantalla_crear_cuenta(self):
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Crear Nueva Cuenta", font=("Arial", 18, "bold"), fg="#0a2342").pack(pady=20)
        
        tk.Label(self.root, text="Nombre completo:").pack()
        nombre_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        nombre_entry.pack(pady=5)
        
        tk.Label(self.root, text="PIN (4 digitos):").pack()
        pin_entry = tk.Entry(self.root, width=40, font=("Arial", 12), show="*")
        pin_entry.pack(pady=5)
        
        tk.Label(self.root, text="Saldo inicial: $").pack()
        saldo_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        saldo_entry.pack(pady=5)
        
        def crear():
            nombre = nombre_entry.get().strip()
            pin = pin_entry.get().strip()
            saldo_text = saldo_entry.get().strip()
            
            if not nombre:
                messagebox.showwarning("Atencion", "Escribe tu nombre")
                return
            if len(pin) != 4 or not pin.isdigit():
                messagebox.showwarning("Atencion", "El PIN debe tener 4 digitos")
                return
            
            try:
                saldo = float(saldo_text)
                if saldo < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Atencion", "Ingresa un monto valido")
                return
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            numero_cuenta = str(len(cuentas) + 1).zfill(6)
            
            nueva = {
                "nombre": nombre,
                "numero_cuenta": numero_cuenta,
                "pin": pin,
                "saldo": saldo,
                "tipo": "Ahorros"
            }
            
            cuentas.append(nueva)
            guardar_datos(ARCHIVO_CUENTAS, cuentas)
            
            if saldo > 0:
                registrar_transaccion(numero_cuenta, "Deposito inicial", saldo)
            
            messagebox.showinfo("Exito", "Cuenta creada con exito!\nNumero de cuenta: " + numero_cuenta)
            self.pantalla_inicio()
        
        tk.Button(self.root, text="Crear Cuenta", command=crear,
                  bg="#27ae60", fg="white", font=("Arial", 12), width=20).pack(pady=20)
        tk.Button(self.root, text="Volver", command=self.pantalla_inicio,
                  font=("Arial", 10)).pack(pady=5)
    
    def pantalla_iniciar_sesion(self):
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Iniciar Sesion", font=("Arial", 18, "bold"), fg="#0a2342").pack(pady=20)
        
        tk.Label(self.root, text="Numero de cuenta:").pack()
        cuenta_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        cuenta_entry.pack(pady=5)
        
        tk.Label(self.root, text="PIN:").pack()
        pin_entry = tk.Entry(self.root, width=40, font=("Arial", 12), show="*")
        pin_entry.pack(pady=5)
        
        intentos = [0]
        max_intentos = 3
        
        def entrar():
            num_cuenta = cuenta_entry.get().strip()
            pin = pin_entry.get().strip()
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            for c in cuentas:
                if c["numero_cuenta"] == num_cuenta and c["pin"] == pin:
                    self.cuenta_actual = c
                    messagebox.showinfo("Bienvenido", "Hola, " + c["nombre"] + "!")
                    self.menu_principal()
                    return
            
            intentos[0] += 1
            restantes = max_intentos - intentos[0]
            if restantes > 0:
                messagebox.showwarning("Error", "Datos incorrectos.\nLe quedan " + str(restantes) + " intentos")
            else:
                messagebox.showerror("Bloqueado", "Demasiados intentos fallidos")
                self.pantalla_inicio()
        
        tk.Button(self.root, text="Entrar", command=entrar,
                  bg="#0a2342", fg="white", font=("Arial", 12), width=20).pack(pady=20)
        tk.Button(self.root, text="Volver", command=self.pantalla_inicio,
                  font=("Arial", 10)).pack(pady=5)
    
    def menu_principal(self):
        self.limpiar_pantalla()
        
        nombre = self.cuenta_actual["nombre"]
        saldo = self.cuenta_actual["saldo"]
        num_cuenta = self.cuenta_actual["numero_cuenta"]
        
        tk.Label(self.root, text=nombre, font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(self.root, text="Cuenta: " + num_cuenta, font=("Arial", 10), fg="#555").pack()
        tk.Label(self.root, text="${:,.2f}".format(saldo), font=("Arial", 22, "bold"), fg="#27ae60").pack(pady=15)
        
        tk.Frame(self.root, height=2, bg="#ddd").pack(fill="x", padx=20, pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        btn_style = {"font": ("Arial", 11), "width": 22, "height": 2, "pady": 5}
        
        tk.Button(frame, text="Depositar", bg="#f39c12", fg="white",
                  command=self.pantalla_depositar, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(frame, text="Retirar", bg="#e74c3c", fg="white",
                  command=self.pantalla_retirar, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Transferir", bg="#3498db", fg="white",
                  command=self.pantalla_transferir, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        
        tk.Button(frame, text="Historial", bg="#9b59b6", fg="white",
                  command=self.pantalla_historial, **btn_style).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Cambiar PIN", bg="#1abc9c", fg="white",
                  command=self.pantalla_cambiar_pin, **btn_style).grid(row=2, column=0, padx=5, pady=5)
        
        tk.Button(frame, text="Cerrar Sesion", bg="#95a5a6", fg="white",
                  command=self.cerrar_sesion, **btn_style).grid(row=2, column=1, padx=5, pady=5)
    
    def actualizar_saldo_actual(self):
        cuentas = cargar_datos(ARCHIVO_CUENTAS)
        for c in cuentas:
            if c["numero_cuenta"] == self.cuenta_actual["numero_cuenta"]:
                self.cuenta_actual = c
                break
    
    def pantalla_depositar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Depositar")
        ventana.geometry("350x200")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="Monto a depositar: $", font=("Arial", 12)).pack(pady=20)
        monto_entry = tk.Entry(ventana, width=25, font=("Arial", 12))
        monto_entry.pack(pady=5)
        
        def aceptar():
            try:
                monto = float(monto_entry.get())
            except ValueError:
                messagebox.showwarning("Atencion", "Ingresa un monto valido")
                return
            if monto <= 0:
                messagebox.showwarning("Atencion", "El monto debe ser mayor a 0")
                return
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            for c in cuentas:
                if c["numero_cuenta"] == self.cuenta_actual["numero_cuenta"]:
                    c["saldo"] += monto
                    break
            guardar_datos(ARCHIVO_CUENTAS, cuentas)
            registrar_transaccion(self.cuenta_actual["numero_cuenta"], "Deposito", monto)
            self.actualizar_saldo_actual()
            messagebox.showinfo("Exito", "Deposito realizado.\nNuevo saldo: ${:,.2f}".format(self.cuenta_actual["saldo"]))
            ventana.destroy()
            self.menu_principal()
        
        tk.Button(ventana, text="Aceptar", command=aceptar, bg="#27ae60", fg="white", width=12).pack(pady=10)
        tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=12).pack()
    
    def pantalla_retirar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Retirar")
        ventana.geometry("350x220")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="Saldo disponible: ${:,.2f}".format(self.cuenta_actual["saldo"]), font=("Arial", 11), fg="#555").pack(pady=10)
        tk.Label(ventana, text="Monto a retirar: $", font=("Arial", 12)).pack(pady=5)
        monto_entry = tk.Entry(ventana, width=25, font=("Arial", 12))
        monto_entry.pack(pady=5)
        
        def aceptar():
            try:
                monto = float(monto_entry.get())
            except ValueError:
                messagebox.showwarning("Atencion", "Ingresa un monto valido")
                return
            if monto <= 0:
                messagebox.showwarning("Atencion", "El monto debe ser mayor a 0")
                return
            if monto > self.cuenta_actual["saldo"]:
                messagebox.showwarning("Atencion", "Fondos insuficientes")
                return
            if monto % 1000 != 0:
                messagebox.showwarning("Atencion", "Debe ser multiplo de $1.000")
                return
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            for c in cuentas:
                if c["numero_cuenta"] == self.cuenta_actual["numero_cuenta"]:
                    c["saldo"] -= monto
                    break
            guardar_datos(ARCHIVO_CUENTAS, cuentas)
            registrar_transaccion(self.cuenta_actual["numero_cuenta"], "Retiro", monto)
            self.actualizar_saldo_actual()
            messagebox.showinfo("Exito", "Retiro realizado.\nNuevo saldo: ${:,.2f}".format(self.cuenta_actual["saldo"]))
            ventana.destroy()
            self.menu_principal()
        
        tk.Button(ventana, text="Aceptar", command=aceptar, bg="#27ae60", fg="white", width=12).pack(pady=10)
        tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=12).pack()
    
    def pantalla_transferir(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Transferir")
        ventana.geometry("380x300")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="Cuenta destino:", font=("Arial", 12)).pack(pady=10)
        destino_entry = tk.Entry(ventana, width=30, font=("Arial", 12))
        destino_entry.pack(pady=5)
        
        tk.Label(ventana, text="Monto a transferir: $", font=("Arial", 12)).pack(pady=10)
        monto_entry = tk.Entry(ventana, width=30, font=("Arial", 12))
        monto_entry.pack(pady=5)
        
        def aceptar():
            destino = destino_entry.get().strip()
            if destino == self.cuenta_actual["numero_cuenta"]:
                messagebox.showwarning("Atencion", "No puedes transferir a tu propia cuenta")
                return
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            cuenta_destino = None
            for c in cuentas:
                if c["numero_cuenta"] == destino:
                    cuenta_destino = c
                    break
            if not cuenta_destino:
                messagebox.showwarning("Atencion", "La cuenta destino no existe")
                return
            
            try:
                monto = float(monto_entry.get())
            except ValueError:
                messagebox.showwarning("Atencion", "Monto invalido")
                return
            if monto <= 0 or monto > self.cuenta_actual["saldo"]:
                messagebox.showwarning("Atencion", "Monto invalido o fondos insuficientes")
                return
            
            for c in cuentas:
                if c["numero_cuenta"] == self.cuenta_actual["numero_cuenta"]:
                    c["saldo"] -= monto
                if c["numero_cuenta"] == destino:
                    c["saldo"] += monto
            
            guardar_datos(ARCHIVO_CUENTAS, cuentas)
            registrar_transaccion(self.cuenta_actual["numero_cuenta"], "Transferencia enviada", monto, destino)
            registrar_transaccion(destino, "Transferencia recibida", monto, self.cuenta_actual["numero_cuenta"])
            self.actualizar_saldo_actual()
            messagebox.showinfo("Exito", "Transferencia realizada.\nEnviaste ${:,.2f} a {}".format(monto, cuenta_destino["nombre"]))
            ventana.destroy()
            self.menu_principal()
        
        tk.Button(ventana, text="Aceptar", command=aceptar, bg="#27ae60", fg="white", width=12).pack(pady=15)
        tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=12).pack()
    
    def pantalla_historial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Transacciones")
       
        ventana.geometry("600x400")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="Historial de Transacciones", font=("Arial", 14, "bold")).pack(pady=10)
        
        marco = tk.Frame(ventana)
        marco.pack(fill="both", expand=True, padx=10)
        
        columnas = ("fecha", "tipo", "monto")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12)
        
        tabla.heading("fecha", text="Fecha y Hora")
        tabla.heading("tipo", text="Tipo")
        tabla.heading("monto", text="Monto")
        
        tabla.column("fecha", width=150)
        tabla.column("tipo", width=250)
        tabla.column("monto", width=150)
        
        scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        
        tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        
        transacciones = cargar_datos(ARCHIVO_TRANSACCIONES)
        mi_historial = [t for t in transacciones if t["cuenta"] == self.cuenta_actual["numero_cuenta"]]
        
        if not mi_historial:
            tabla.insert("", "end", values=("Sin movimientos aun", "", ""))
        else:
            for t in reversed(mi_historial):
                tabla.insert("", "end", values=(t["fecha"], t["tipo"], "${:,.2f}".format(t["monto"])))
        
        tk.Button(ventana, text="Cerrar", command=ventana.destroy, width=15).pack(pady=10)
    
    def pantalla_cambiar_pin(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Cambiar PIN")
        ventana.geometry("350x250")
        ventana.resizable(False, False)
        
        tk.Label(ventana, text="PIN actual:", font=("Arial", 12)).pack(pady=10)
        pin_actual_entry = tk.Entry(ventana, width=25, font=("Arial", 12), show="*")
        pin_actual_entry.pack(pady=5)
        
        tk.Label(ventana, text="Nuevo PIN (4 digitos):", font=("Arial", 12)).pack(pady=10)
        nuevo_pin_entry = tk.Entry(ventana, width=25, font=("Arial", 12), show="*")
        nuevo_pin_entry.pack(pady=5)
        
        tk.Label(ventana, text="Confirmar nuevo PIN:", font=("Arial", 12)).pack(pady=10)
        confirmar_entry = tk.Entry(ventana, width=25, font=("Arial", 12), show="*")
        confirmar_entry.pack(pady=5)
        
        def aceptar():
            pin_actual = pin_actual_entry.get().strip()
            nuevo = nuevo_pin_entry.get().strip()
            confirmar = confirmar_entry.get().strip()
            
            cuentas = cargar_datos(ARCHIVO_CUENTAS)
            
            if pin_actual != self.cuenta_actual["pin"]:
                messagebox.showwarning("Atencion", "El PIN actual es incorrecto")
                return
            if len(nuevo) != 4 or not nuevo.isdigit():
                messagebox.showwarning("Atencion", "El nuevo PIN debe tener 4 digitos")
                return
            if nuevo != confirmar:
                messagebox.showwarning("Atencion", "Los PIN no coinciden")
                return
            
            for c in cuentas:
                if c["numero_cuenta"] == self.cuenta_actual["numero_cuenta"]:
                    c["pin"] = nuevo
                    self.cuenta_actual["pin"] = nuevo
                    break
            
            guardar_datos(ARCHIVO_CUENTAS, cuentas)
            messagebox.showinfo("Exito", "PIN actualizado correctamente")
            ventana.destroy()
        
        tk.Button(ventana, text="Aceptar", command=aceptar, bg="#27ae60", fg="white", width=12).pack(pady=15)
        tk.Button(ventana, text="Cancelar", command=ventana.destroy, width=12).pack()
    
    def cerrar_sesion(self):
        self.cuenta_actual = None
        self.pantalla_inicio()

# ========== EJECUTAR LA APLICACION ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
