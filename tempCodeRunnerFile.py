

root.geometry(f"{background_image.width()}x{background_image.height()}+350+180")

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_font = font.Font(family="Helvetica", size=16, weight="bold")
button_font = font.Font(family="Helvetica", size=10, weight="bold")

welcome_label = tk.Label(root, text="Welcome to AI Gym Trainer", bg='black', fg='white', font=("Helvetica", 15))
welcome_label.place(x=20, y=20)

prompt_label = tk.Label(root, text="Select an exercise you would like to train?", bg='black', fg='white', font=("Helvetica", 13))
prompt_label.place(x=20, y=60)

button1 = tk.Button(root, text="Single Dumbbell Curl", command=lambda: execute_exercise("1"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button1.place(x=20, y=100, width=220, height=30)

button2 = tk.Button(root, text="Reverse Fly", command=lambda: execute_exercise("2"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button2.place(x=20, y=140, width=220, height=30)

button3 = tk.Button(root, text="Barbell Curl", command=lambda: execute_exercise("3"), bg='grey20', fg='white', font=button_font, relief=tk.RAISED, bd=5)
button3.place(x=20, y=180, width=220, height=30)