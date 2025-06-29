def func_ini_mutasi(angka: int) -> None:
    """
    Fungsi ini menerima sebuah kalimat dan mencetaknya dengan huruf kapital.
    """
    angka += 1

angka_awal = 5
print(f"=== Sebelum mutasi: {angka_awal} ===")
func_ini_mutasi(angka_awal)
print(f"=== Setelah mutasi: {angka_awal} ===")