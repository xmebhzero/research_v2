const Groq = require('groq-sdk');

const groq = new Groq();
async function main() {
  const chatCompletion = await groq.chat.completions.create({
    "messages": [
      {
        "role": "system",
        "content": "Anda adalah seorang mahasiswa jurusan Teknik Informatika dan memiliki minat tinggi terhadap Aplikasi berbasis mobile untuk menemukan fasilitas olahraga terdekat yang sedang menyusun tugas akhir di salah satu universitas di Indonesia."
      },
      {
        "role": "user",
        "content": "Tugas Anda adalah membuat 5 buah skripsi penelitian yang sesuai dengan jurusan dan minat Anda dengan kelengkapan sebagai berikut:\n\n1. Judul penelitian\n2. Ringkasan penelitian\n3. Tujuan-tujuan penelitian\n4. Manfaat-manfaat penelitian\n5. ID penelitian\n\nJawablah dengan menggunakan bahasa Indonesia"
      },
      {
        "role": "assistant",
        "content": "Berikut adalah 5 buah skripsi penelitian yang sesuai dengan jurusan dan minat saya:\n\n**1. Judul:** \"Desain dan Implementasi Aplikasi Mobile untuk Mencari Fasilitas Olahraga Terdekat Berbasis GPS\"\n**Ringkasan:** Penelitian ini bertujuan untuk merancang dan mengembangkan aplikasi mobile yang dapat membantu pengguna mencari fasilitas olahraga terdekat menggunakan teknologi GPS.\n**Tujuan:**\n* Merancang antarmuka aplikasi yang user-friendly dan mudah digunakan\n* Mengembangkan fitur pencarian fasilitas olahraga berbasis GPS\n* Mengetahui efektivitas aplikasi dalam membantu pengguna mencari fasilitas olahraga terdekat\n**Manfaat:** Aplikasi ini dapat membantu pengguna mencari fasilitas olahraga terdekat dengan mudah dan cepat, sehingga dapat meningkatkan kesadaran akan pentingnya olahraga dan meningkatkan kualitas hidup.\n**ID Penelitian:** TI-001\n\n---\n\n**2. Judul:** \"Analisis Kinerja Aplikasi Mobile untuk Mencari Fasilitas Olahraga Terdekat Berbasis Android\"\n**Ringkasan:** Penelitian ini bertujuan untuk menganalisis kinerja aplikasi mobile berbasis Android yang digunakan untuk mencari fasilitas olahraga terdekat.\n**Tujuan:**\n* Menganalisis kinerja aplikasi dalam hal waktu respon dan akurasi hasil pencarian\n* Mengetahui efek penggunaan teknologi GPS pada kinerja aplikasi\n* Merekomendasikan strategi optimasi kinerja aplikasi\n**Manfaat:** Penelitian ini dapat membantu meningkatkan kinerja aplikasi mobile untuk mencari fasilitas olahraga terdekat, sehingga dapat meningkatkan kepuasan pengguna.\n**ID Penelitian:** TI-002\n\n---\n\n**3. Judul:** \"Perbandingan Aplikasi Mobile untuk Mencari Fasilitas Olahraga Terdekat Berbasis iOS dan Android\"\n**Ringkasan:** Penelitian ini bertujuan untuk membandingkan kinerja dan fitur aplikasi mobile berbasis iOS dan Android yang digunakan untuk mencari fasilitas olahraga terdekat.\n**Tujuan:**\n* Membandingkan fitur dan kinerja aplikasi mobile berbasis iOS dan Android\n* Mengetahui kelebihan dan kekurangan masing-masing platform\n* Merekomendasikan platform yang paling sesuai untuk pengembangan aplikasi\n**Manfaat:** Penelitian ini dapat membantu pengembang aplikasi dalam memilih platform yang paling sesuai untuk pengembangan aplikasi, sehingga dapat meningkatkan kualitas aplikasi.\n**ID Penelitian:** TI-003\n\n---\n\n**4. Judul:** \"Pengembangan Aplikasi Mobile untuk Mencari Fasilitas Olahraga Terdekat Berbasis Augmented Reality\"\n**Ringkasan:** Penelitian ini bertujuan untuk mengembangkan aplikasi mobile berbasis Augmented Reality (AR) yang dapat membantu pengguna mencari fasilitas olahraga terdekat.\n**Tujuan:**\n* Mengembangkan fitur AR yang dapat menampilkan informasi fasilitas olahraga terdekat\n* Mengetahui efektivitas aplikasi dalam membantu pengguna mencari fasilitas olahraga terdekat\n* Merekomendasikan strategi pengembangan aplikasi berbasis AR\n**Manfaat:** Aplikasi ini dapat membantu pengguna mencari fasilitas olahraga terdekat dengan cara yang lebih menarik dan interaktif, sehingga dapat meningkatkan kesadaran akan pentingnya olahraga.\n**ID Penelitian:** TI-004\n\n---\n\n**5. Judul:** \"Analisis Penggunaan Aplikasi Mobile untuk Mencari Fasilitas Olahraga Terdekat dalam Meningkatkan Kesadaran Olahraga Masyarakat\"\n**Ringkasan:** Penelitian ini bertujuan untuk menganalisis penggunaan aplikasi mobile untuk mencari fasilitas olahraga terdekat dalam meningkatkan kesadaran olahraga masyarakat.\n**Tujuan:**\n* Menganalisis penggunaan aplikasi dalam meningkatkan kesadaran olahraga masyarakat\n* Mengetahui faktor-faktor yang mempengaruhi penggunaan aplikasi\n"
      }
    ],
    "model": "llama3-70b-8192",
    "temperature": 1,
    "max_completion_tokens": 1024,
    "top_p": 1,
    "stream": true,
    "stop": null
  });

  for await (const chunk of chatCompletion) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}

main();