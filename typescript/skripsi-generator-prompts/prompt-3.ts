const Groq = require('groq-sdk');

const groq = new Groq();
async function main() {
  const chatCompletion = await groq.chat.completions.create({
    "messages": [
      {
        "role": "system",
        "content": "Anda adalah seorang mahasiswa jurusan Teknik Informatika dan memiliki minat tinggi terhadap Smart home yang sedang menyusun tugas akhir di salah satu universitas di Indonesia."
      },
      {
        "role": "user",
        "content": "Tugas Anda adalah membuat 5 buah skripsi penelitian yang sesuai dengan jurusan dan minat Anda dengan kelengkapan sebagai berikut:\n\n1. Judul penelitian\n2. Ringkasan penelitian\n3. Tujuan-tujuan penelitian\n4. Manfaat-manfaat penelitian\n5. ID penelitian\n\nJawablah dengan menggunakan bahasa Indonesia."
      },
      {
        "role": "assistant",
        "content": "Berikut adalah 5 buah skripsi penelitian yang sesuai dengan jurusan Teknik Informatika dan minat pada Smart Home:\n\n**1. Judul:** \"Desain dan Implementasi Sistem Kendali Rumah Pintar Berbasis IoT menggunakan NodeMCU dan Blynk\"\n**Ringkasan:** Penelitian ini bertujuan untuk merancang dan mengimplementasikan sistem kendali rumah pintar berbasis IoT menggunakan NodeMCU dan Blynk. Sistem ini dapat mengontrol peralatan rumah tangga secara remote menggunakan smartphone dan memantau kondisi rumah secara real-time.\n**Tujuan:** (1) Merancang sistem kendali rumah pintar berbasis IoT, (2) Mengimplementasikan sistem kendali rumah pintar menggunakan NodeMCU dan Blynk, (3) Menguji coba sistem kendali rumah pintar berbasis IoT.\n**Manfaat:** (1) Meningkatkan kenyamanan dan keamanan rumah tangga, (2) Menghemat energi dan sumber daya, (3) Meningkatkan efisiensi penggunaan peralatan rumah tangga.\n**ID Penelitian:** TI-001\n\n**2. Judul:** \"Pengembangan Sistem Monitoring Kualitas Udara dalam Rumah Pintar menggunakan Sensor MQ-135 dan ESP32\"\n**Ringkasan:** Penelitian ini bertujuan untuk mengembangkan sistem monitoring kualitas udara dalam rumah pintar menggunakan sensor MQ-135 dan ESP32. Sistem ini dapat memantau kualitas udara secara real-time dan memberikan peringatan jika kualitas udara tidak memenuhi standar.\n**Tujuan:** (1) Mengembangkan sistem monitoring kualitas udara dalam rumah pintar, (2) Mengintegrasikan sensor MQ-135 dan ESP32 dalam sistem monitoring, (3) Menguji coba sistem monitoring kualitas udara.\n**Manfaat:** (1) Meningkatkan kesehatan dan kenyamanan penghuni rumah, (2) Meningkatkan kesadaran akan pentingnya kualitas udara, (3) Meningkatkan efisiensi penggunaan sistem ventilasi.\n**ID Penelitian:** TI-002\n\n**3. Judul:** \"Analisis Kinerja Sistem Keamanan Rumah Pintar Berbasis Face Recognition menggunakan Raspberry Pi dan OpenCV\"\n**Ringkasan:** Penelitian ini bertujuan untuk menganalisis kinerja sistem keamanan rumah pintar berbasis face recognition menggunakan Raspberry Pi dan OpenCV. Sistem ini dapat mengenali wajah penghuni rumah dan memberikan akses atau penolakan secara otomatis.\n**Tujuan:** (1) Menganalisis kinerja sistem keamanan rumah pintar berbasis face recognition, (2) Mengintegrasikan Raspberry Pi dan OpenCV dalam sistem keamanan, (3) Menguji coba sistem keamanan rumah pintar.\n**Manfaat:** (1) Meningkatkan keamanan rumah tangga, (2) Meningkatkan kenyamanan penghuni rumah, (3) Meningkatkan efisiensi penggunaan sistem keamanan.\n**ID Penelitian:** TI-003\n\n**4. Judul:** \"Desain dan Implementasi Sistem Kendali Penerangan Rumah Pintar Berbasis IoT menggunakan ESP8266 dan MQTT\"\n**Ringkasan:** Penelitian ini bertujuan untuk merancang dan mengimplementasikan sistem kendali penerangan rumah pintar berbasis IoT menggunakan ESP8266 dan MQTT. Sistem ini dapat mengontrol penerangan rumah secara remote menggunakan smartphone dan memantau kondisi penerangan secara real-time.\n**Tujuan:** (1) Merancang sistem kendali penerangan rumah pintar berbasis IoT, (2) Mengimplementasikan sistem kendali penerangan rumah pintar menggunakan ESP8266 dan MQTT, (3) Menguji coba sistem kendali penerangan rumah pintar.\n**Manfaat:** (1) Meningkatkan kenyamanan dan keamanan rumah tangga, (2) Menghemat energi dan sumber daya, (3) Meningkatkan efisiensi penggunaan penerangan.\n**ID Penelitian:** TI-004\n\n**5. Judul:** \"Pengembangan Sistem Kendali Temperatur Rumah Pintar Berbasis IoT menggunakan Arduino dan Wi-Fi\"\n**Ringkasan:** Penelitian ini bertujuan untuk mengembangkan sistem kendali temperatur rumah pintar berbasis IoT menggunakan Arduino dan Wi-Fi. Sistem ini dapat"
      }
    ],
    "model": "llama3-70b-8192",
    "temperature": 1,
    "max_completion_tokens": 1024,
    "top_p": 1,
    "stream": false,
    "stop": null
  });

   console.log(chatCompletion.choices[0].message.content);
}

main();