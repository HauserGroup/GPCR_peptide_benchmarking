# Import libraries
import pandas as pd
import pathlib
import plotly.graph_objects as go

# Create Dummy Data
# phases = ["Visit", "Sign-up", "Selection", "Purchase", "Review", "Test"]
# values = [13873, 10553, 5443, 3703, 1708]

phases = [
    "Human target",
    "Peptide ligand",
    "Human source",
    "With sequence",
    "GPCR target",
    "Agonist",
]
# where labels start
different_y_vals = [280, 270, 260, 240, 230, 90]
values = [1488, 790, 762, 728, 475, 446]
save_path = pathlib.Path("plots/figure1_abstract/funnel.svg")
data = {"phases": phases, "values": values}
df = pd.DataFrame(data)


# HELPER FUNCTION: For annotation text
def style_link(text, link, **settings):
    style = ";".join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
    return f'<a href="{link}" style="{style}">{text}</a>'


def get_color_range(start_col, end_col, n):
    """
    Create a range of n colors between start_col and end_col.
    start_col: str, for example: "rgb(17,81,133)"
    end_col: str, for example: "rgb(0,142,215)"
    n: int, number of colors to generate

    returns, list of strings, for example: ["rgb(17,81,133)", "rgb(16,82,133)", ...]
    """
    start_col = start_col.replace("rgb(", "").replace(")", "")
    start_col = [int(x) for x in start_col.split(",")]

    end_col = end_col.replace("rgb(", "").replace(")", "")
    end_col = [int(x) for x in end_col.split(",")]

    colors = []
    for i in range(n):
        new_col = []
        for j in range(3):
            diff = end_col[j] - start_col[j]
            step = diff / n
            new_col.append(int(start_col[j] + (step * i)))
        colors.append(f"rgb({new_col[0]},{new_col[1]},{new_col[2]})")

    return colors


# MAIN FUNCTION: input a dataframe
def plot(df, annotation=None):
    phases = df["phases"]
    values = df["values"]

    required_colors = len(phases) - 1
    # make a spectrum of colors
    start_color = "rgb(17,81,133)"
    end_color = "rgb(0,142,215)"
    final_color = "rgb(0,0,0)"
    colors_in_range = [start_color] * required_colors
    colors_in_range = get_color_range(start_color, end_color, required_colors)
    print(colors_in_range)
    colors = colors_in_range + [final_color]

    n_phase = len(phases)
    plot_height = 400
    section_w = 100
    section_d = 10
    unit_height = plot_height / max(values)
    phase_h = [int(value * unit_height) for value in values]
    width = section_w * n_phase + section_d * (n_phase - 1)
    shapes = []
    label_x = []

    for i in range(n_phase):
        if i == n_phase - 1:
            points = [phase_h[i] / 2, width, phase_h[i] / 2, width - section_w]
            max_final = points[1]
            midpoint_final = max_final / 2
            path = f"M -{max_final} 0 L -{midpoint_final} {midpoint_final} L 0 0 L -{midpoint_final} -{midpoint_final} Z"
        else:
            points = [phase_h[i] / 2, width, phase_h[i + 1] / 2, width - section_w]
            path = f"M -{points[1]} {points[0]} L -{points[3]} {points[2]} L -{points[3]} -{points[2]} L -{points[1]} -{points[0]} Z"
        outline_color = "rgb(13, 47, 65)"
        shape = {
            "type": "path",
            "path": path,
            "fillcolor": colors[i],
            "layer": "below",
            # outline color
            "line": {"width": 2, "color": outline_color},
        }
        shapes.append(shape)
        label_x.append((width - (section_w / 2)) * -1)
        width -= section_w + section_d

    label_trace = go.Scatter(
        x=label_x,
        y=[210] * n_phase,
        mode="text",
        text=["" for _ in range(n_phase)],
        textfont=dict(color="rgba(44,58,71,1)", size=15),
    )

    value_trace = go.Scatter(
        x=label_x,
        y=[0] * n_phase,
        mode="text",
        text=values,
        textfont=dict(
            color="rgba(256,256,256,1)",
            size=15,
        ),
    )

    data = [label_trace, value_trace]

    layout = go.Layout(
        title="Horizontal Funnel Chart",
        shapes=shapes,
        height=800,
        width=560,
        showlegend=False,
        xaxis=dict(showticklabels=False, zeroline=False, showgrid=False),
        yaxis=dict(
            showticklabels=False,
            zeroline=False,
            showgrid=False,
            scaleanchor="x",
            scaleratio=1,
        ),
    )
    # add rotated phase labels
    fig = go.Figure(data=data, layout=layout)

    for i, phase in enumerate(phases):
        textangle = 45
        if i == n_phase - 1:
            textangle = 0
        fig.add_annotation(
            x=label_x[i],
            y=different_y_vals[i],
            text=phase,
            textangle=textangle,
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font=dict(color="rgba(44,58,71,1)", size=15),
        )
    # save to save path
    fig.write_image(save_path)


plot(df)
