import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles


TEMP = "temp_files"
with open(f"{TEMP}/selection_from.txt", "r") as f:
    edges1 = set(line.strip() for line in f)
with open(f"{TEMP}/selection_to.txt", "r") as f:
    edges2 = set(line.strip() for line in f)
edges = edges1.intersection(edges2)
print(len(edges1), len(edges1) - len(edges))
print(len(edges2), len(edges2) - len(edges))
print(
    len(edges),
)

fig, ax = plt.subplots(figsize=(3, 3))
ax.set_title("Ielas datu kopu šķēlums (A ∩ B)", fontsize=10, fontweight="bold", pad=2)

v = venn2(subsets=[edges1, edges2], set_labels=("A", "B"), set_colors=("w", "w"), ax=ax)
v.get_label_by_id("10").set_x(-0.25)
v.get_label_by_id("01").set_x(0.25)
v.get_label_by_id("11").set_x(0)
v.set_labels[0].set_position((-0.25, -0.4))
v.set_labels[1].set_position((0.25, -0.4))

c = venn2_circles(subsets=(2, 2, 2), linestyle="solid", ax=ax)
c[0].set_radius(0.32)
c[1].set_radius(0.32)
c[0].set_lw(2.0)
c[1].set_lw(2.0)
c[0].set_color("green")
c[1].set_color("red")
c[0].set_alpha(0.5)
c[1].set_alpha(0.5)
c[0].set_edgecolor("black")
c[1].set_edgecolor("black")

fig.tight_layout(pad=0.05)
plt.show()
