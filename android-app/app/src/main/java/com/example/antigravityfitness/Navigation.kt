package com.example.antigravityfitness

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.runtime.rememberNavBackStack
import androidx.navigation3.ui.NavDisplay
import com.example.antigravityfitness.data.DefaultDataRepository
import com.example.antigravityfitness.ui.main.FormScreen
import com.example.antigravityfitness.ui.main.MainScreenUiState
import com.example.antigravityfitness.ui.main.MainScreenViewModel
import com.example.antigravityfitness.ui.main.ResultsScreen

@Composable
fun MainNavigation() {
  val backStack = rememberNavBackStack(Main)
  val viewModel: MainScreenViewModel = viewModel { MainScreenViewModel(DefaultDataRepository()) }

  NavDisplay(
    backStack = backStack,
    onBack = { backStack.removeLastOrNull() },
    entryProvider =
      entryProvider {
        entry<Main> {
          val state by viewModel.uiState.collectAsState()
          
          if (state is MainScreenUiState.Success) {
            val plan = (state as MainScreenUiState.Success).plan
            ResultsScreen(
              plan = plan,
              onBack = { viewModel.reset() },
              modifier = Modifier.safeDrawingPadding()
            )
          } else {
            FormScreen(
              isLoading = state is MainScreenUiState.Loading,
              errorMessage = (state as? MainScreenUiState.Error)?.message,
              onSubmit = { profile -> viewModel.generatePlan(profile) },
              modifier = Modifier.safeDrawingPadding()
            )
          }
        }
      },
  )
}
