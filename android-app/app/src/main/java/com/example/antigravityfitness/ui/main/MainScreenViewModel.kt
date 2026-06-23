package com.example.antigravityfitness.ui.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.antigravityfitness.data.DataRepository
import com.example.antigravityfitness.data.UserProfile
import com.example.antigravityfitness.data.WorkoutPlan
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MainScreenViewModel(private val dataRepository: DataRepository) : ViewModel() {

  private val _uiState = MutableStateFlow<MainScreenUiState>(MainScreenUiState.Idle)
  val uiState: StateFlow<MainScreenUiState> = _uiState.asStateFlow()

  fun generatePlan(profile: UserProfile) {
    viewModelScope.launch {
      _uiState.value = MainScreenUiState.Loading
      try {
        val plan = dataRepository.generateWorkoutPlan(profile)
        _uiState.value = MainScreenUiState.Success(plan)
      } catch (e: Exception) {
        _uiState.value = MainScreenUiState.Error(e.message ?: "Unknown error")
      }
    }
  }

  fun reset() {
    _uiState.value = MainScreenUiState.Idle
  }
}

sealed interface MainScreenUiState {
  object Idle : MainScreenUiState
  object Loading : MainScreenUiState
  data class Error(val message: String) : MainScreenUiState
  data class Success(val plan: WorkoutPlan) : MainScreenUiState
}
