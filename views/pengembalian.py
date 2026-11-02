import streamlit as st
from datetime import date
from core import db
from views.common import header, loan_rows

def render():
    header("RETURN PROCESS","Pengembalian","Proses pengembalian barang sewaan dan perbarui stok secara otomatis.")
    rows=loan_rows("p.status='Dipinjam'")
    if not rows:
        st.success("Tidak ada penyewaan aktif saat ini."); return
    for r in rows:
        terlambat=r["tanggal_rencana_kembali"] < date.today().isoformat()
        with st.container(border=True):
            a,b,c=st.columns([2,3,1.4])
            a.markdown(f'**{r["kode"]}**\n\n{r["nama"]}')
            b.write(f'Barang: {r["barang"] or "-"}')
            b.caption(f'Rencana kembali: {r["tanggal_rencana_kembali"]}')
            if terlambat: c.warning("Terlambat")
            if c.button("Proses kembali",key=f'return_{r["id"]}',type="primary"):
                try: db.return_loan(r["id"]); st.success(f'Transaksi {r["kode"]} berhasil dikembalikan.'); st.rerun()
                except Exception as e: st.error(str(e))
