package com.example.antigravityfitness.ui.main

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.antigravityfitness.data.FitnessLevel
import com.example.antigravityfitness.data.Goal
import com.example.antigravityfitness.data.UserProfile
import com.example.antigravityfitness.theme.Blue500

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FormScreen(
    isLoading: Boolean,
    errorMessage: String?,
    onSubmit: (UserProfile) -> Unit,
    modifier: Modifier = Modifier
) {
    var age by remember { mutableStateOf("25") }
    var weight by remember { mutableStateOf("75") }
    var fitnessLevel by remember { mutableStateOf(FitnessLevel.INTERMEDIATE) }
    var goal by remember { mutableStateOf(Goal.MUSCLE_GAIN) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "🚀 ANTIGRAVITY ENGINE",
            color = Blue500,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            letterSpacing = 2.sp,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        Text(
            text = "Profilini Oluştur",
            color = Color.White,
            fontSize = 32.sp,
            fontWeight = FontWeight.ExtraBold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        Text(
            text = "Bize kendinden bahset, sana en uygun programı hazırlayalım.",
            color = Color.LightGray,
            fontSize = 14.sp,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        Card(
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                OutlinedTextField(
                    value = age,
                    onValueChange = { age = it },
                    label = { Text("Yaş") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp)
                )

                OutlinedTextField(
                    value = weight,
                    onValueChange = { weight = it },
                    label = { Text("Kilo (kg)") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(8.dp)
                )

                DropdownMenuField(
                    label = "Spor Seviyesi",
                    options = listOf(
                        "Başlangıç" to FitnessLevel.BEGINNER,
                        "Orta" to FitnessLevel.INTERMEDIATE,
                        "İleri" to FitnessLevel.ADVANCED
                    ),
                    selectedOption = fitnessLevel,
                    onOptionSelected = { fitnessLevel = it }
                )

                DropdownMenuField(
                    label = "Hedef",
                    options = listOf(
                        "Kas Gelişimi" to Goal.MUSCLE_GAIN,
                        "Kilo Verme" to Goal.WEIGHT_LOSS,
                        "Dayanıklılık" to Goal.ENDURANCE
                    ),
                    selectedOption = goal,
                    onOptionSelected = { goal = it }
                )

                Spacer(modifier = Modifier.height(16.dp))

                Button(
                    onClick = {
                        val ageInt = age.toIntOrNull() ?: 25
                        val weightDouble = weight.toDoubleOrNull() ?: 75.0
                        onSubmit(UserProfile(ageInt, weightDouble, fitnessLevel, goal))
                    },
                    enabled = !isLoading,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    if (isLoading) {
                        CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                    } else {
                        Text("Program Oluştur", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    }
                }

                if (errorMessage != null) {
                    Text(
                        text = errorMessage,
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun <T> DropdownMenuField(
    label: String,
    options: List<Pair<String, T>>,
    selectedOption: T,
    onOptionSelected: (T) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    val selectedText = options.firstOrNull { it.second == selectedOption }?.first ?: ""

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = !expanded }
    ) {
        OutlinedTextField(
            value = selectedText,
            onValueChange = {},
            readOnly = true,
            label = { Text(label) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            modifier = Modifier
                .menuAnchor()
                .fillMaxWidth(),
            shape = RoundedCornerShape(8.dp)
        )
        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            options.forEach { (text, value) ->
                DropdownMenuItem(
                    text = { Text(text) },
                    onClick = {
                        onOptionSelected(value)
                        expanded = false
                    }
                )
            }
        }
    }
}
