import customtkinter as ctk 

# configuração aparência
ctk.set_appearance_mode('dark')

#criação da janela principal
app = ctk.CTk()
app.title('Sistema de estoque')
app.geometry('400x350')

#criação dos campos
#label
label_usuario = ctk.CTkLabel(app,text='Usuário:')
label_usuario.pack(pady=10)
#entry
campo_usuario = ctk.CTkEntry(app,placeholder_text='Digite o seu usuário')
campo_usuario.pack(pady=10)
#label
label_senha = ctk.CTkLabel(app,text='Senha:')
label_senha.pack(pady=10)
#entry
campo_senha = ctk.CTkEntry(app,placeholder_text='Digite a sua senha')
campo_senha.pack(pady=10)
#button
ctk.CTkButton(app,text='Login')


#iniciar o app
app.mainloop()