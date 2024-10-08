const getPopCheckResponse = {
  code: 200,
  message: "success!",
  data: {
    questions: [
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "MULTI_SELECT",
        tags: "Others",
        question:
          "Kegiatan apa yang pernah Anda lakukan ketika menggunakan platform e-commerce/marketplace/digital payment dalam 3 bulan terakhir?",
        category: "MANDATORY",
        validAsPrioritizedUntil: null,
        label: "DigitalAppsActivity",
        expiredIn: 1,
        options: [
          {
            value: "Membeli produk fisik",
            isExclusiveOption: false,
          },
          {
            value: "Membeli produk digital",
            isExclusiveOption: false,
          },
          {
            value: "Membeli produk fintech",
            isExclusiveOption: false,
          },
          {
            value: "Menjual produk",
            isExclusiveOption: false,
          },
          {
            value: "Menjadi reseller/agen",
            isExclusiveOption: false,
          },
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "MULTI_SELECT",
        tags: "Lifestyle",
        question: "TEST",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "Testdoang",
        expiredIn: 10,
        options: [
          {
            value: "ini random",
            isExclusiveOption: false,
          },
          {
            value: "ini juga boleh",
            isExclusiveOption: false,
          },
          {
            value: "ini boleh pilihin",
            isExclusiveOption: false,
          },
          {
            value: "ini exclusive",
            isExclusiveOption: true,
          },
        ],
        isRandomOrder: true,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Basic",
        question: "Status Pernikahan",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "MaritalStatus",
        expiredIn: 1,
        options: [
          "Belum menikah (Sendiri)",
          "Belum menikah (Tinggal serumah dengan pacar atau partner)",
          "Menikah, tapi tinggal terpisah",
          "Menikah, serumah, tapi tidak memiliki anak",
          "Menikah, serumah, dan mempunyai anak",
          "Becerai/janda/duda dan mempunyai anak",
          "Becerai/janda/duda dan tidak mempunyai anak",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Basic",
        question: "Apa pendidikan terakhir kamu?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "HighestEducation",
        expiredIn: 1,
        options: [
          "Tidak ada pendidikan formal",
          "Sekolah Dasar",
          "Sekolah Menengah Pertama (SMP)",
          "Sekolah Menengah Atas (SMA)",
          "Akademi (D1/D2/D3) / Setingkatnya",
          "Sarjana S1",
          "Magister S2",
          "Doktor S3",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Others",
        question:
          "Tempat belanja mana saja yang PALING SERING Anda kunjungi dalam 6 bulan terakhir? Belanja di sini tidak terbatas pada belanja bulanan (groceries), tetapi juga termasuk belanja harian untuk barang/produk yang tidak dibeli dalam belanja bulanan",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "ShoppingCentresMostOften",
        expiredIn: 7,
        options: [
          "Hypermarket (Hypermart, Transmart, Lotte Mart, dsb.)",
          "Supermarket (Giant, Superindo, TipTop, Hari-Hari, Yogya, dsb.)",
          "Minimarket (Alfamart, Indomaret, dsb.)",
          "Convenience store (Circle K, FamilyMart)",
          "Warung biasa",
          "Saya belanja online (online shop, e-commerce)",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "MULTI_SELECT",
        tags: "Others",
        question:
          "Tempat belanja mana saja yang biasa Anda kunjungi dalam 6 bulan terakhir? Belanja di sini tidak terbatas pada belanja bulanan (groceries), tetapi juga termasuk belanja harian untuk barang/produk yang tidak dibeli dalam belanja bulanan",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "ShoppingCentres",
        expiredIn: 7,
        options: [
          {
            value: "Hypermarket (Hypermart, Transmart, Lotte Mart, dsb.)",
            isExclusiveOption: false,
          },
          {
            value:
              "Supermarket (Giant, Superindo, TipTop, Hari-Hari, Yogya, dsb.)",
            isExclusiveOption: false,
          },
          {
            value: "Minimarket (Alfamart, Indomaret, dsb.)",
            isExclusiveOption: false,
          },
          {
            value: "Convenience store (Circle K, FamilyMart)",
            isExclusiveOption: false,
          },
          {
            value: "Warung biasa",
            isExclusiveOption: false,
          },
          {
            value: "Saya belanja online (online shop, e-commerce)",
            isExclusiveOption: false,
          },
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Others",
        question: "Jabatan Pekerjaan",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "Occupation",
        expiredIn: 1,
        options: [
          "Wiraswasta, pemilik, atau rekanan",
          "President/CEO/Chairperson",
          "Middle Management",
          "Chief Financial Officer (CFO)",
          "Senior Management",
          "Director",
          "HR Manager",
          "Product Manager",
          "Supply Manager",
          "Project Management",
          "Sales Manager",
          "Business Administrator",
          "Supervisor",
          "Karyawan biasa (admin, resepsionis, kasir, pramuniaga, security)",
          "Karyawan pemula (management trainee, junior staff, dsb.)",
          "Pegawai Negeri Sipil/BUMN",
          "Mandor",
          "Staf teknik",
          "Faculty Staff",
          "Staf Penjualan/sales",
          "Chief Technical Officer (CTO)",
          "C-level executive lainnya (selain CTO, CFO, CEO)",
          "Perajin/seniman",
          "Buyer/Purchasing Agent",
          "Manajer/direktur keuangan",
          "Manajer/direktur gedung",
          "Manajer/direktur fasilitas",
          "Manajer/direktur teknologi informasi",
          "Manajer/direktur layanan kesehatan",
          "Manajer/direktur perhotelan, ritel, layanan lainnya",
          "Profesional kesehatan (dokter, perawat, apoteker)",
          "Profesional laboratorium",
          "Profesional sosial dan budaya",
          "Profesional hukum (penasihat hukum, paralegal, pengacara)",
          "Pekerja perawatan pribadi/jasa perlindungan",
          "Staf penjualan (misalnya, staf penjualan di toko dan pasar)",
          "Pekerja kehutanan atau perikanan",
          "Pekerja pertanian",
          "Supir (mobil, truk)",
          "Ojek online (motor/mobil)",
          "Operator pabrik/mesin, operator mesin berat",
          "Ahli teknologi perawatan kesehatan, Administrator perawatan kesehatan",
          "Buruh terlatih (tukang ledeng, montir, tukang listrik, tukang kayu, dsb.)",
          "Buruh tidak terlatih (buruh pabrik)",
          "Polri/TNI/militer",
          "Penasihat keuangan dan investasi",
          "Analis keuangan",
          "Analis sistem",
          "Pengembang perangkat lunak",
          "Pengembang web dan multimedia",
          "Programmer aplikasi (misalnya, pengembang aplikasi)",
          "Desainer dan administrator database",
          "Administrator sistem",
          "Administrator jaringan",
          "Teknisi meja bantuan",
          "Teknisi jaringan dan sistem komputer",
          "Arsitek/konsultan TI lainnya",
          "Buruh bangunan",
          "Kontraktor",
          "Tukang batu",
          "Tukang kayu",
          "Pekerja atap",
          "Teknisi lantai/ubin/wallpaper/cat",
          "Tukang ledeng atau pemasang pipa",
          "Arsitektur, insinyur, dan profesional sains",
          "Manajer/direktur produksi/layanan khusus",
          "Kerja serabutan",
          "Saya tidak bekerja",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "CITIES",
        participantType: "DETAILED_ADDRESS",
        tags: "BasicProfile",
        question: "Tempat Tinggal Saat Ini",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "Domicile",
        expiredIn: 1,
        options: [],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Profesi",
        question: "Departemen Pekerjaan",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "JobDepartment",
        expiredIn: 10,
        options: ["Hi mika", "bisa ga"],
        isRandomOrder: true,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Family",
        question: "Jika Anda memiliki anak, berapa anak yang anda miliki?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "NumberOfChildren",
        expiredIn: 1,
        options: ["Tidak ada", "Satu", "Dua", "Tiga", "Empat atau lebih"],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "BasicProfile",
        question: "Apa bahan bakar memasak yang anda gunakan?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "CookingFuel",
        expiredIn: 1,
        options: [
          "Kompor Listrik",
          "Gas Elpiji 12 KG/Gas 5 KG/Gas 7 KG",
          "Gas Elpiji - 3 KG",
          "Gas Alam/Kota",
          "Minyak Tanah",
          "Kayu Bakar      ",
          "Arang",
          "Bukan PerempuanBriket",
          "Lainnya",
          "Tidak memasak",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "RANGE",
        participantType: "INPUT_DATE",
        tags: "Others",
        question: "Ayam date nih? gimana?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "AyamDate",
        expiredIn: 1,
        options: [],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Others",
        question: "Test Delete Parent 1",
        category: "OPTIONAL",
        validAsPrioritizedUntil: null,
        label: "TestDeleteParent_1",
        expiredIn: 30,
        options: ["Iya", "Tidak"],
        isRandomOrder: false,
        conditions: {
          AyamDate: {
            EQUAL: ["2022-01-01"],
          },
        },
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Profesi",
        question: "apa profesi yang Anda inginkan ?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "profesi",
        expiredIn: 10,
        options: ["Dokter", "Arsitek"],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Basic",
        question: "Single Criteria 1 Updated",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "Single1Updated",
        expiredIn: 10,
        options: [
          "Opsi A",
          "Opsi B",
          "Opsi baru setelah published 1",
          "Opsi baru setelah published 2",
          "Opsi baru setelah published 3",
          "Opsi baru setelah published 4",
          "Opsi baru setelah published 5",
          "Opsi baru setelah published 5",
          "Opsi baru setelah published 5",
        ],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Basic",
        question: "Apakah Kamu / Istri Kamu Sedang Hamil?",
        category: "ADDITIONAL",
        validAsPrioritizedUntil: null,
        label: "ExpectingParent",
        expiredIn: 1,
        options: ["Iya", "Tidak"],
        isRandomOrder: false,
      },
      {
        optionType: "MULTIPLE_OPTION",
        participantType: "OPTION_SELECT",
        tags: "Basic",
        question: "Single Criteria 3",
        category: "OPTIONAL",
        validAsPrioritizedUntil: null,
        label: "Single3",
        expiredIn: 10,
        options: ["Opsi A", "Opsi B"],
        isRandomOrder: false,
      },
    ],
    totalAnsweredQuestions: 14,
    eligibleToJoinStudy: false,
    totalQuestions: 43,
  },
};

function getAnswer() {
  const { data } = getPopCheckResponse;
  const { questions } = data;

  const payload = {};

  for (const question of questions) {
    const { label, options, participantType } = question;

    if (participantType === "INPUT_NUMBER") {
      payload[label] = [1];
    } else if (participantType === "INPUT_DATE") {
      payload[label] = ["2022-01-02"];
    } else if (options[0] && options[0].value) {
      payload[label] = [options[0].value];
    } else if (participantType === "DETAILED_ADDRESS") {
      const address = {
        province: "Bali",
        city: "Badung",
        district: "Abiansemal",
        subdistrict: "Abiansemal",
        zipCode: "80352",
      };

      payload[label] = [
        address.city,
        address.province,
        address.district,
        address.subdistrict,
        address.zipCode,
      ];
    } else {
      payload[label] = [options[0]];
    }
  }

  console.log(JSON.stringify(payload));
}

getAnswer();
