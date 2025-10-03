# Apa itu MCP?
MCP adalah sebuah protokol yang menstandarisasi komunikasi / hubungan antar LLM atau aplikasi AI.
Bisa dikatakan, MCP ini seperti port USB-C pada laptop, yang dapat terhubung ke beberapa device seperti mouse, external harddrive, dan device-device lain.
USB-C disini adalah protokol, laptop adalah host dan juga client. Dan device-device yang terhubung ini, adalah MCP server.

# Arsitektur MCP

MCP Host (dengan beberapa MCP Client) -> MCP Servers
MCP Host adalah laptop
MCP Client adalah port atau lubang yang mensupport protokol USB-C
MCP Server adalah device-device yang memberikan fungsi atau layanannya sendiri (seperti hdd memberikan akses ke data external, mouse yang memberikan tool calling untuk mengubah posisi cursor dll)

## Komponen MCP Server

### Tools
Sebuah fungsi yang dapat dieksekusi atau dipanggil oleh MCP Client untuk melakukan suatu task, seperti membaca file dari GDrive, mendapatkan data perkiraan cuaca, membuat survey, dan lain sebagainya

### Resources
Sama seperti GET request pada HTTP, dimana MCP Server menyediakan dokumen-dokumen yang dapat dilihat dan di query oleh MCP Client, sehingga apabila dibutuhkan, MCP Client bisa mendapatkan context tambahan sebelum melakukan sesuatu. Contoh data yang bisa diberikan oleh MCP Server meliputi file (docx, pdf, txt, dll), database records atau http response (json).

### Prompt Templates
Sebuah prompt yang sudah dibuat sebelumnya oleh MCP Server, agar MCP Client tidak perlu membuat lagi membuat prompt nya sendiri