package com.zaneschepke.wireguardautotunnel.desktop.ui.state

import com.zaneschepke.wireguardautotunnel.client.domain.model.TunnelConfig

data class TunnelsUiState(
    val tunnels: List<TunnelConfig> = emptyList(),
    val selectedTunnels: List<TunnelConfig> = emptyList(),
    val isSelectionMode: Boolean = false,
    val isLoaded: Boolean = false,
)
