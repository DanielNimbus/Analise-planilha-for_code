import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Carregar planilha ===
df = pd.read_csv("analisar.csv")

print(df)

# === Separar apenas as colunas numéricas (notas 1-5) ===
df_numeric = df.select_dtypes(include=["number"])

# === Criar pasta de saída ===
output_dir = "analise_resultados"
os.makedirs(output_dir, exist_ok=True)

# === 1. Heatmap (áreas no eixo Y, pessoas no X) ===
plt.figure(figsize=(12, 8))
sns.heatmap(
    df_numeric.T,  # transposto
    cmap="YlGnBu",
    annot=True,
    cbar_kws={'label': 'Nível (1-5)'},
    xticklabels=df["Nome"].apply(lambda x: " ".join(x.split()[:3])),
    yticklabels=df_numeric.columns
)
plt.title("Heatmap - Conhecimentos por Área")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "heatmap_conhecimentos.png"))
plt.close()

# === 2. Média por área (barras) ===
media_areas = df_numeric.mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
media_areas.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Conhecimento médio por área")
plt.ylabel("Média (1-5)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "media_por_area.png"))
plt.close()

# === 3. Ranking de top instrutores por área ===
top_instrutores = {}
for col in df_numeric.columns:
    top = df[["Nome", col]].sort_values(by=col, ascending=False).head(8)
    top_instrutores[col] = top

# === 4. Salvar informações em arquivo de texto (formatado) ===
with open(os.path.join(output_dir, "resumo_instrutores.txt"), "w", encoding="utf-8") as f:
    f.write("=== Ranking de Top Instrutores por Área ===\n\n")
    for area, tabela in top_instrutores.items():
        f.write(f"--- {area} (Média: {media_areas[area]:.2f}) ---\n")
        for _, row in tabela.iterrows():
            f.write(f"{row['Nome']:<20} Nota: {row[area]}\n")
        f.write("\n")

    f.write("\n=== Médias Gerais ===\n")
    for area, media in media_areas.items():
        f.write(f"{area:<25}: {media:.2f}\n")

print(f"Resultados salvos em: {output_dir}")
