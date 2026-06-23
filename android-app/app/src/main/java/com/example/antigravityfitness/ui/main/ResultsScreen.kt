package com.example.antigravityfitness.ui.main

import android.content.Intent
import android.net.Uri
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.antigravityfitness.data.Exercise
import com.example.antigravityfitness.data.WorkoutDay
import com.example.antigravityfitness.data.WorkoutPlan
import com.example.antigravityfitness.theme.AccentColor

@Composable
fun ResultsScreen(
    plan: WorkoutPlan,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text(
                text = plan.plan_name,
                fontSize = 28.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color.White
            )
            Text(
                text = plan.description,
                fontSize = 14.sp,
                color = Color.LightGray,
                modifier = Modifier.padding(vertical = 8.dp)
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem(plan.days_per_week.toString(), "Gün / Hafta")
                StatItem(plan.days.sumOf { it.estimated_duration_min }.toString(), "Toplam Dk")
                StatItem(plan.days.sumOf { it.total_calories }.toString(), "Tahmini kcal")
            }
        }

        items(plan.days) { day ->
            DayCard(day)
        }

        item {
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = onBack,
                modifier = Modifier.fillMaxWidth().height(56.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("🔄 Yeniden Oluştur", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun StatItem(value: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = value, fontSize = 24.sp, fontWeight = FontWeight.Bold, color = AccentColor)
        Text(text = label, fontSize = 12.sp, color = Color.Gray)
    }
}

@Composable
fun DayCard(day: WorkoutDay) {
    var expanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
    ) {
        Column {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { expanded = !expanded }
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(text = day.day, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    Text(
                        text = "🕒 ${day.estimated_duration_min} dk • 🔥 ${day.total_calories} kcal • 🎯 ${day.focus}",
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                }
                Text(
                    text = if (expanded) "▲" else "▼",
                    color = Color.Gray,
                    fontSize = 16.sp
                )
            }

            AnimatedVisibility(visible = expanded) {
                Column(modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
                    day.exercises.forEach { ex ->
                        ExerciseRow(ex)
                        HorizontalDivider(color = Color.DarkGray, modifier = Modifier.padding(vertical = 8.dp))
                    }
                }
            }
        }
    }
}

@Composable
fun ExerciseRow(exercise: Exercise) {
    val context = LocalContext.current

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(text = exercise.icon, fontSize = 24.sp, modifier = Modifier.padding(end = 8.dp))
            Column {
                Text(text = exercise.exercise_name, fontWeight = FontWeight.Bold, color = Color.White)
                Text(text = "${exercise.sets} set • ${exercise.reps} • Dinlenme: ${exercise.rest_time}", fontSize = 12.sp, color = Color.LightGray)
            }
        }

        TextButton(onClick = {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(exercise.tutorial_video_url))
            context.startActivity(intent)
        }) {
            Text("▶ İzle", color = AccentColor)
        }
    }
}
