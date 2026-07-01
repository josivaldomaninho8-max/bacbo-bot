import logging

logger = logging.getLogger(__name__)

class BacBoAnalyzer:
    def __init__(self):
        self.history = []
        self.max_history = 50
    
    def analyze(self, results: list) -> dict:
        """Analisa os resultados e retorna o sinal"""
        if not results:
            return {
                "signal": "📊 Aguardando dados...",
                "confidence": 0,
                "details": "Sem resultados disponíveis"
            }
        
        # Atualizar histórico
        self.history.extend(results)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        # Analisar últimos resultados
        recent = results[:10]
        counts = {"B": 0, "P": 0, "T": 0}
        
        for result in recent:
            if result in counts:
                counts[result] += 1
        
        total = len(recent)
        
        # Calcular porcentagens
        percentages = {
            "B": (counts["B"] / total * 100) if total > 0 else 0,
            "P": (counts["P"] / total * 100) if total > 0 else 0,
            "T": (counts["T"] / total * 100) if total > 0 else 0
        }
        
        # Determinar sinal
        max_type = max(percentages, key=percentages.get)
        max_percent = percentages[max_type]
        
        # Emojis e nomes
        names = {"B": "🔵 BANCO", "P": "🔴 JOGADOR", "T": "🟡 EMPATE"}
        
        if max_percent >= 50:
            signal = f"{names[max_type]} - {max_percent:.1f}% chance"
            confidence = "ALTA"
        elif max_percent >= 40:
            signal = f"{names[max_type]} - {max_percent:.1f}% chance"
            confidence = "MÉDIA"
        else:
            # Sem tendência clara, recomendar o mais quente
            signal = f"📈 {names[max_type]} - Tendência detectada"
            confidence = "BAIXA"
        
        return {
            "signal": signal,
            "confidence": confidence,
            "counts": counts,
            "percentages": percentages,
            "recent_results": recent[:10],
            "total_analyzed": len(self.history)
        }
    
    def format_message(self, analysis: dict) -> str:
        """Formata a análise para envio no Telegram"""
        if not analysis:
            return "⚠️ Erro ao analisar sinais"
        
        recent = ' '.join(analysis['recent_results']) if analysis['recent_results'] else 'Sem dados'
        
        message = f"""
🎯 *SINAL BAC BO - ELEPHANTBET*

📊 *Análise:* {analysis['signal']}
📈 *Confiança:* {analysis['confidence']}

📋 *Detalhes:*
• Banco: {analysis['counts']['B']} ({analysis['percentages']['B']:.1f}%)
• Jogador: {analysis['counts']['P']} ({analysis['percentages']['P']:.1f}%)
• Empate: {analysis['counts']['T']} ({analysis['percentages']['T']:.1f}%)

📈 *Últimos resultados:* {recent}
📊 *Total analisado:* {analysis['total_analyzed']}

⏰ *Atualizado:* {self._get_timestamp()}
        """
        return message
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp atual formatado"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
