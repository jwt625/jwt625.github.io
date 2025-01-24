


# %% interactive cone
import numpy as np
import plotly.graph_objects as go

# Create polar coordinates for circular boundary
k_max = 2  # Maximum wavevector magnitude
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, k_max, 50)

# Create grid in polar coordinates
T, R = np.meshgrid(theta, r)

# Convert to Cartesian coordinates
k_x = R * np.cos(T)
k_y = R * np.sin(T)

# Calculate omega values for upper cone
omega = np.sqrt(k_x**2 + k_y**2)

# Create figure with minimal styling
fig = go.Figure(go.Surface(
    x=k_x, 
    y=k_y, 
    z=omega,
    colorscale='Viridis',
    opacity=0.5,  # Increased transparency
    showscale=False,  # Disable colorbar
    hoverinfo='none'  # Disable hover info
))

# Configure ultra-clean layout
fig.update_layout(
    title='Light Cone',
    scene=dict(
        xaxis=dict(
            title='kₓ',
            showticklabels=False,
            ticks=""
        ),
        yaxis=dict(
            title='kᵧ',
            showticklabels=False,
            ticks=""
        ),
        zaxis=dict(
            title='ω',
            showticklabels=False,
            ticks=""
        ),
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    width=800,
    height=600
)

# Show plot
fig.show()




# %% onto a lattice
import numpy as np
import plotly.graph_objects as go

# Base cone parameters
k_max = 11  # Cone base radius
shift = 4  # Lattice constant

# Generate base cone coordinates (polar)
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, k_max, 50)
T, R = np.meshgrid(theta, r)
kx_base = R * np.cos(T)
ky_base = R * np.sin(T)
# omega_base = np.sqrt(kx_base**2 + ky_base**2)

# quadratic dispersion
omega_base = (kx_base**2 + ky_base**2)/k_max

# Create lattice points (3x3 grid)
lattice_points = [(i*shift, j*shift) for i in [-2, -1, 0, 1, 2] 
                                for j in [-2, -1, 0, 1, 2]]

# Create figure
fig = go.Figure()

# Add multiple translated cones
for dx, dy in lattice_points:
    fig.add_trace(go.Surface(
        x=kx_base + dx,
        y=ky_base + dy,
        z=omega_base,
        colorscale='Viridis',
        showscale=False,
        opacity=0.25,  # Increased transparency
        hoverinfo='none'
    ))

# Configure ultra-clean layout with expanded view
n_plotRange = 0.5
fig.update_layout(
    title='Photonic Crystal-like Light Cone Array',
    scene=dict(
        xaxis=dict(
            title='kₓ',
            showticklabels=False,
            ticks="",
            range=[-shift*n_plotRange, shift*n_plotRange]  # Expanded view
        ),
        yaxis=dict(
            title='kᵧ',
            showticklabels=False,
            ticks="",
            range=[-shift*n_plotRange, shift*n_plotRange]
        ),
        zaxis=dict(
            title='ω',
            showticklabels=False,
            ticks="",
            range=[0, k_max*0.5]
        ),
        camera=dict(eye=dict(x=2, y=2, z=0.8)),
        aspectmode='manual',  # Changed from 'cube'
        aspectratio=dict(
            x=1,   # Relative x-axis size
            y=1,   # Relative y-axis size
            z=3    # Stretch factor for z-axis (ω)
        )
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    width=800,
    height=1000
)

# Show plot
fig.show()






############## test interactive plot
#%%
%matplotlib widget


#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Enable interactive mode
plt.ion()

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust layout for sliders

x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x))

# Add sliders
slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(slider_ax, 'Frequency', 0.1, 5.0, valinit=1.0)

def update(val):
    line.set_ydata(np.sin(slider.val * x))
    fig.canvas.draw_idle()  # Update plot without redrawing everything

slider.on_changed(update)
plt.show()

# %%
import plotly.graph_objs as go
from plotly.subplots import make_subplots

fig = make_subplots()
fig.add_trace(go.Scatter(x=[1,2,3], y=[4,5,6]))
fig.update_layout(
    sliders=[{
        "steps": [{"args": [{"y": [i, i+1, i+2]}], "label": i} for i in range(10)]
    }]
)

fig.write_html("../_includes/plot.html", include_plotlyjs="cdn")



# %% phase matching of refraction

import plotly.graph_objects as go
import numpy as np

# Generate circle points (static data)
theta = np.linspace(0, 2*np.pi, 100)
circle1_x = np.cos(theta)
circle1_y = np.sin(theta)
circle2_x = 1.5 * np.cos(theta)
circle2_y = 1.5 * np.sin(theta)

# Create figure with static elements
fig = go.Figure()

# Add persistent circles with legend entries
fig.add_trace(go.Scatter(
    x=circle1_x, y=circle1_y,
    mode='lines',
    line=dict(color='gray', dash='dot'),
    name='n₁ (Medium 1)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=circle2_x, y=circle2_y,
    mode='lines', 
    line=dict(color='gray', dash='dash'),
    name='n₂ (Medium 2)',
    showlegend=True
))

# Add permanent legend entries for vectors (never displayed)
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='blue', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₁/k<sub>0</sub> (Refracted)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='red', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₂/k<sub>0</sub> (Incident)',
    showlegend=True
))

# Initialize dynamic elements (hidden from legend)
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₁
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₂
fig.add_trace(go.Scatter(x=[], y=[], mode='text', showlegend=False))  # status

# Create frames with proper arrow angles
frames = []
theta2_values = np.linspace(0, np.pi/2, 100)

for theta2 in theta2_values:
    k2_x = 1.5 * np.cos(theta2)
    k2_y = 1.5 * np.sin(theta2)
    
    # Calculate angles for arrow orientation (degrees)
    angle_k2 = np.degrees(theta2)
    
    # Phase matching calculation
    if k2_x <= 1.0:
        theta1 = np.arccos(k2_x)
        k1_x, k1_y = np.cos(theta1), np.sin(theta1)
        angle_k1 = np.degrees(theta1)
        status = "Phase Matched"
        status_color = "green"
    else:
        k1_x, k1_y = np.nan, np.nan
        angle_k1 = 0
        status = "Total Internal Reflection"
        status_color = "red"

    frame = go.Frame(
        data=[
            # Static circles (preserve original data)
            go.Scatter(x=circle1_x, y=circle1_y),
            go.Scatter(x=circle2_x, y=circle2_y),
            # k₁ vector
            go.Scatter(
                x=[0, k1_x], y=[0, k1_y],
                line=dict(color='blue', width=2),
                marker=dict(
                    symbol='arrow',
                    size=15,
                    angleref='previous',
                    # angle=angle_k1  # Offset for arrow orientation
                )
            ),
            # k₂ vector
            go.Scatter(
                x=[0, k2_x], y=[0, k2_y],
                line=dict(color='red', width=2),
                marker=dict(
                    symbol='arrow',
                    size=15,
                    angleref='previous',
                    # angle=angle_k2  # Offset for arrow orientation
                )
            ),
            # Status text
            go.Scatter(
                x=[0], y=[1.7],
                mode='text',
                text=[f"<b>{status}</b>"],
                textfont=dict(color=status_color, size=14)
            )
        ],
        name=f"theta_{np.rad2deg(theta2):.1f}"
    )
    frames.append(frame)

# Assign frames to figure
fig.frames = frames

# Configure slider and layout
slider = [dict(
    active=0,
    currentvalue=dict(prefix="θ₂: ", font=dict(size=14)),
    pad=dict(t=50),
    steps=[dict(
        method='animate',
        args=[
            [f"theta_{np.rad2deg(theta2):.1f}"],
            dict(mode='immediate', 
                 frame=dict(duration=100, redraw=True),
                 transition=dict(duration=0))
        ],
        label=f"{np.rad2deg(theta2):.1f}°"
    ) for theta2 in theta2_values]
)]

fig.update_layout(
    title="Phase Matching Condition Demo<br><sub>Adjust θ₂ with slider below</sub>",
    xaxis=dict(
        range=[-1.8, 1.8],
        title="k<sub>x</sub>",
        scaleanchor="y",
        scaleratio=1
    ),
    yaxis=dict(
        range=[-0.1, 1.8],
        title="k<sub>y</sub>"
    ),
    showlegend=True,
    legend=dict(
        x=1.05,
        y=0.5,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,0,0,0.2)',
        traceorder='normal'
    ),
    sliders=slider,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        x=0.1,
        y=0,
        buttons=[dict(
            label='▶',
            method='animate',
            args=[None, dict(frame=dict(duration=100, redraw=True), 
                            fromcurrent=True)]
        )]
    )]
)

# Save to HTML
fig.write_html(
    "../_includes/phase_matching_plot.html",
    include_plotlyjs='cdn',
    full_html=False
)


# %%
