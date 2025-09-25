"""
Plotting utilities for glacial cycle simulations.

Functions
---------
- plot_state_model(time, insolation, states, i0, i1, i3, LR04_time=None, LR04_iso=None, 
                   EDC_time=None, EDC_iso=None, title="Climate State Model", savepath=None):
    Plot results of a glacial state model simulation.

- plot_icevol_model(time, insolation, forcing, ice_volume, states, vR, LR04_time=None,
                    LR04_iso=None, EDC_time=None, EDC_iso=None, title="Ice Volume Model",
                    savepath=None):
    Plot results of a glacial ice volume model simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import List 
from .models.base import GlacialState


def plot_state_model(
    time: np.ndarray,
    insolation: np.ndarray,
    states: List[GlacialState],
    i0: float,
    i1: float,
    i3: float,
    LR04_time=None,
    LR04_iso=None,
    EDC_time=None,
    EDC_iso=None,
    title: str = "Climate State Model",
):
    """
    Plot results of a glacial state model simulation.

    Parameters
    ----------
    - time : np.ndarray
        Array of time points.
    - insolation : np.ndarray
        Insolation values corresponding to `time`.
    - states : List[GlacialState]
        Model states over time.
    - i0, i1, i3 : float
        Thresholds for state transitions.
    - LR04_time, LR04_iso : optional
        Time and δ18O proxy data from LR04 stack.
    - EDC_time, EDC_iso : optional
        Time and δ18O proxy data from EDC core.
    - title : str, optional
        Plot title.
    - savepath : str, optional
        Path to save the figure.

    Returns
    -------
    - fig : matplotlib.figure.Figure
        Figure object.
    - axs : np.ndarray
        Array of axes objects.
    """
    gs = dict(hspace=0)
    fig, axs = plt.subplots(4, 1, sharex=True, gridspec_kw=gs)

    # Insolation + thresholds
    Os = np.zeros_like(time)
    yticks = [i0, i1, i3]
    ylabels = [r"$i_0$", r"$i_1 = i_2$", r"$i_3$"]

    i=0
    ax_r = axs[i].secondary_yaxis("right")
    ax_r.set_yticks(yticks, ylabels)
    axs[i].set_title(title)
    axs[i].plot(-time, Os + i3, "k--", lw=0.7)
    axs[i].plot(-time, Os + i1, "k-", lw=0.7)
    axs[i].plot(-time, Os + i0, "k-.", lw=0.7)
    axs[i].plot(-time, insolation, "k")
    axs[i].set_ylabel("Insolation")
    i+=1

    # Model states
    yticks = [0, 1, 2]
    ylabels = ["G", "g", "i"]
    axs[i].plot(-time, [s.value for s in states], "k")
    axs[i].set_yticks(yticks, ylabels)
    axs[i].yaxis.set_label_position("right")
    axs[i].yaxis.tick_right()
    axs[i].set_ylabel("Model state")
    axs[i].set_xlim(0, len(time))
    axs[i].set_ylim(-0.2, 2.2)
    i+=1

    # Proxy records
    if LR04_time is not None and LR04_iso is not None:
        axs[i].set_title("LR04 ", loc="right", y=-0.02, fontsize=10)
        axs[i].set_ylabel(r"$\delta O^{18}$ (‰)")
        axs[i].plot(-LR04_time, LR04_iso, "grey", label="LR04")
        axs[i].set_ylim(axs[i].get_ylim()[::-1])
        axs[i].set_xlabel("Time before present [kyr]")
        i+=1

    if EDC_time is not None and EDC_iso is not None:
        axs[i].set_title("EDC ", loc="right", y=-0.02, fontsize=10)
        axs[i].plot(-EDC_time, EDC_iso, "grey", label="EDC")
        axs[i].yaxis.set_label_position("right")
        axs[i].yaxis.tick_right()
        axs[i].set_ylabel(r"$\delta O^{18}$ (‰)")
        axs[i].set_xlabel("Time before present [kyr]")

    for ax in axs:
        if not ax.has_data():   # True if nothing plotted
            fig.delaxes(ax)

    # Force bottom axis to show labels
    fig.axes[-1].set_xlabel("Time before present [kyr]")
    fig.axes[-1].tick_params(labelbottom=True)
    return fig, axs


def plot_icevol_model(
    time: np.ndarray,
    insolation: np.ndarray,
    forcing: np.ndarray,
    ice_volume: List[float],
    states: List[GlacialState],
    vR: np.ndarray,
    LR04_time=None,
    LR04_iso=None,
    EDC_time=None,
    EDC_iso=None,
    title: str = "Ice Volume Model",
):
    """
    Plot results of a glacial ice volume model simulation.

    Parameters
    ----------
    - time : np.ndarray
        Array of time points.
    - insolation : np.ndarray
        Insolation values.
    - forcing : np.ndarray
        Forcing used in the ice volume model.
    - ice_volume : List[float]
        Ice volume over time.
    - states : List[GlacialState]
        Model states over time.
    - vR : np.ndarray
        State-dependent reference ice volume.
    - LR04_time, LR04_iso : optional
        LR04 δ18O proxy data.
    - EDC_time, EDC_iso : optional
        EDC δ18O proxy data.
    - title : str, optional
        Plot title.
    - savepath : str, optional
        Path to save the figure.

    Returns
    -------
    - fig : matplotlib.figure.Figure
        Figure object.
    - axs : np.ndarray
        Array of axes objects.
    """
    gs = dict(hspace=0)
    fig, axs = plt.subplots(4, 1, sharex=True, gridspec_kw=gs)
    i = 0

    # Insolation + forcing
    axs[i].plot(-time, forcing, "k")
    axs[i].plot(-time, insolation, "k:", lw=0.8)
    axs[i].set_xlim(0, len(insolation))
    axs[i].set_ylabel("Insolation")
    axs[i].set_title(title)
    i+=1

    # Ice volume vs. state-dependent vR
    vR_arr = vR[[s.value for s in states]]
    axs[i].plot(-time, vR_arr, "k--", lw=0.7)
    axs[i].plot(-time, ice_volume, "k")
    axs[i].yaxis.set_label_position("right")
    axs[i].yaxis.tick_right()
    axs[i].tick_params(left=False, labelleft=False)
    axs[i].set_ylim(axs[i].get_ylim()[::-1])
    axs[i].set_ylabel("Ice volume")
    i+=1

    # Proxy records
    if LR04_time is not None and LR04_iso is not None:
        axs[i].set_title("LR04 ", loc="right", y=-0.02, fontsize=10)
        axs[i].set_ylabel(r"$\delta O^{18}$ (‰)")
        axs[i].plot(-LR04_time, LR04_iso, "grey", label="LR04")
        axs[i].set_ylim(axs[i].get_ylim()[::-1])
        axs[i].set_xlabel("Time before present [kyr]")
        i+=1

    if EDC_time is not None and EDC_iso is not None:
        axs[i].set_title("EDC ", loc="right", y=-0.02, fontsize=10)
        axs[i].plot(-EDC_time, EDC_iso, "grey", label="EDC")
        axs[i].yaxis.set_label_position("right")
        axs[i].yaxis.tick_right()
        axs[i].set_ylabel(r"$\delta O^{18}$ (‰)")
        axs[i].set_xlabel("Time before present [kyr]")

    for ax in axs:
        if not ax.has_data():   # True if nothing plotted
            fig.delaxes(ax)

    # Force bottom axis to show labels
    fig.axes[-1].set_xlabel("Time before present [kyr]")
    fig.axes[-1].tick_params(labelbottom=True)
    return fig, axs

