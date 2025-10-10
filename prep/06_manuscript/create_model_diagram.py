"""
Model Framework Diagram for Fishing Effort Manuscript
Creates a flowchart showing the two-stage hurdle random forest approach
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(12, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Define colors
color_input = '#E8F4F8'
color_input_border = '#2C5F7C'
color_process = '#FFF4E6'
color_process_border = '#B87A3D'
color_model = '#E8F8E8'
color_model_border = '#2C7C4F'
color_temporal = '#F0E8F8'
color_temporal_border = '#6B4C9A'
color_output = '#FFE8E8'
color_output_border = '#B83D3D'

# Helper function to create boxes
def create_box(ax, x, y, width, height, text, facecolor, edgecolor, fontsize=9, fontweight='normal'):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.1", 
                         facecolor=facecolor, 
                         edgecolor=edgecolor, 
                         linewidth=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, 
            ha='center', va='center', fontsize=fontsize,
            fontweight=fontweight, multialignment='center')

# Helper function to create arrows
def create_arrow(ax, x1, y1, x2, y2, color, linewidth=2, style='solid'):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20,
                           color=color, linewidth=linewidth,
                           linestyle=style)
    ax.add_patch(arrow)


# INPUT DATA section
ax.text(5, 13.2, 'INPUT DATA', ha='center', va='center', 
        fontsize=11, fontweight='bold', color=color_input_border)

# Input boxes (4 across)
create_box(ax, 0.5, 11.5, 2, 1.2, 'AIS Data\n(2015-2024)\nIndustrial vessels',
           color_input, color_input_border)
create_box(ax, 2.7, 11.5, 2, 1.2, 'Satellite Vessel\nDetections\n(2009-2024)\nArtisanal vessels',
           color_input, color_input_border)
create_box(ax, 4.9, 11.5, 2, 1.2, 'Environmental\nPredictors\n(SST, Chl-a, Depth,\nDist. to coast)',
           color_input, color_input_border, fontsize=8)
create_box(ax, 7.1, 11.5, 2, 1.2, 'Governance\nFactors\n(EEZ, Fishing access,\nFAO areas)',
           color_input, color_input_border, fontsize=8)

# MODEL section
ax.text(5, 10.2, 'Country-level two-stage random forest hurdle models', ha='center', va='center',
        fontsize=11, fontweight='bold', color=color_model_border)

# Model stages
create_box(ax, 1, 8.5, 3.5, 1.4, 'Stage 1:\nPresence/Absence\n(classification model)',
           color_model, color_model_border, fontsize=9, fontweight='bold')
create_box(ax, 5.5, 8.5, 3.5, 1.4, 'Stage 2:\nEffort Intensity\n(regression model)',
           color_model, color_model_border, fontsize=9, fontweight='bold')

# Arrows from inputs converging to a midpoint, then to model stages
# Convergence point for Stage 1
convergence_1_y = 10.5
convergence_1_x = 2.75

# Convergence point for Stage 2
convergence_2_y = 10.5
convergence_2_x = 7.25

# Draw arrows from each input box down to their respective convergence points
for x in [1.5, 3.7, 5.9, 8.1]:
    # Arrows to Stage 1 convergence point
    create_arrow(ax, x, 11.5, convergence_1_x, convergence_1_y, color_input_border, linewidth=1.5)
    # Arrows to Stage 2 convergence point
    create_arrow(ax, x, 11.5, convergence_2_x, convergence_2_y, color_input_border, linewidth=1.5)

# Single arrows from convergence points to model boxes
create_arrow(ax, convergence_1_x, convergence_1_y, 2.75, 9.9, color_input_border, linewidth=2.5)
create_arrow(ax, convergence_2_x, convergence_2_y, 7.25, 9.9, color_input_border, linewidth=2.5)


# Exclusion layer box (to feed into temporal predictions)
create_box(ax, 0.4, 6.5, 2.5, 0.9, 'Exclusion Layers:\nSea ice (artisanal and industrial),\nFishing access (industrial only)\nPopulated zones (artisanal only)',
           color_process, color_process_border, fontsize=8)

ax.text(5, 6.5, 'Predictions', ha='center', va='center',
        fontsize=11, fontweight='bold', color=color_temporal_border)

# Temporal predictions and hindcasting
create_box(ax, 2.5, 5, 5, 1.2, 'Temporal predictions and hindcasting\n(1950-2017)',
           color_temporal, color_temporal_border, fontsize=9, fontweight='bold')

# Arrow from stage 2 to temporal
create_arrow(ax, 7.25, 8.5, 5.5, 6.2, color_model_border, linewidth=2.5)
# Arrow from stage 1 to temporal (centered on Stage 1 box)
create_arrow(ax, 2.75, 8.5, 4, 6.2, color_model_border, linewidth=2.5)

# Arrow from exclusion layer to temporal predictions
create_arrow(ax, 3, 6.5, 4, 6.2, color_process_border, linewidth=2, style='dashed')

# Output
create_box(ax, 2, 2.5, 6, 1.8, 'Spatial fishing effort\n1° × 1° resolution\n1950-2017',
           color_output, color_output_border, fontsize=10, fontweight='bold')

# Arrow from temporal to output
create_arrow(ax, 5, 5, 5, 4.3, color_temporal_border, linewidth=3)

plt.tight_layout()
plt.savefig('model_framework_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('model_framework_diagram.pdf', bbox_inches='tight', facecolor='white')

print("Diagram created successfully!")
print("Files saved:")
print("  - model_framework_diagram.png")
print("  - model_framework_diagram.pdf")
