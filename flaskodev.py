from flask import Flask, render_template_string, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask Uygulaması</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
            }
            header {
                position: absolute;
                top: 0;
                right: 0;
                margin: 20px;
            }
            .name {
                color: purple;
                margin-right: 10px; /* Boşluk eklemek için */
            }
            .id {
                color: pink;
            }
            .button {
                display: block;
                margin: 100px auto;
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: darkmagenta;
                border: none;
                cursor: pointer;
                text-align: center;
            }
            .button:hover {
                background-color: purple;
            }
        </style>
    </head>
    <body>
        <header>
            <h1><span class="name">Eda Nur Işık </span><span class="id">No:211213049</span></h1>
        </header>
        <main>
            <button class="button" onclick="generateImage()">Görsel Oluştur</button>
            <div id="image-container"></div>
        </main>
        <script>
            function generateImage() {
                fetch('/generate-image')
                .then(response => response.blob())
                .then(blob => {
                    var url = URL.createObjectURL(blob);
                    var img = document.createElement('img');
                    img.src = url;
                    img.style.display = 'block';
                    img.style.margin = '20px auto';
                    document.getElementById('image-container').innerHTML = '';
                    document.getElementById('image-container').appendChild(img);
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/generate-image')
def generate_image():
    # 1. Adım: Rastgele Koordinatlar Üretme ve Excel Dosyasına Kaydetme
    num_points = 500
    x_coords = np.random.randint(0, 1001, num_points)
    y_coords = np.random.randint(0, 1001, num_points)

    # Bu koordinatları bir DataFrame'e koy
    df = pd.DataFrame({
        'X Koordinatları': x_coords,
        'Y Koordinatları': y_coords
    })

    # DataFrame'i bir Excel dosyasına kaydet
    excel_path = 'koordinatlar.xlsx'
    df.to_excel(excel_path, index=False)

    # 2. Adım: Excel Dosyasını Okuma ve Görselleştirme
    # Excel dosyasını oku
    df = pd.read_excel(excel_path)

    # Koordinatları al
    x_coords = df['X Koordinatları']
    y_coords = df['Y Koordinatları']

    # 200x200 ızgaralara böl ve her ızgaraya rastgele bir renk ata
    grid_size = 200
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'pink']

    plt.figure(figsize=(10, 10))

    for x in range(0, 1000, grid_size):
        for y in range(0, 1000, grid_size):
            # Bu ızgaraya düşen noktaları seç
            mask = (x_coords >= x) & (x_coords < x + grid_size) & (y_coords >= y) & (y_coords < y + grid_size)
            points = df[mask]
            color = np.random.choice(colors)
            plt.scatter(points['X Koordinatları'], points['Y Koordinatları'], color=color)

    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.title('Rastgele Noktaların Görselleştirilmesi')

    # Görseli belleğe kaydet
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
