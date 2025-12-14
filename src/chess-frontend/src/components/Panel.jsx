export default function Panel({ status, loading, turn, fen }) {
  return (
    <div style={{ minWidth: "300px", maxWidth: "380px", background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "16px", boxShadow: "0 2px 6px rgba(0,0,0,0.15)", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ marginBottom: "8px", fontWeight: 600 }}>
        {loading ? "Esperando jugada de la IA..." : status}
      </div>
      <div style={{ marginBottom: "8px" }}>
        Turno: {turn === "w" ? "Blancas" : "Negras"}
      </div>
      <div style={{ fontSize: "12px", color: "#555", wordBreak: "break-all", background: "#f7f7f7", padding: "8px", borderRadius: "6px" }}>
        FEN: {fen}
      </div>
    </div>
  );
}
