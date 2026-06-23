package com.example.antigravityfitness.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
enum class FitnessLevel {
    @SerialName("Beginner") BEGINNER,
    @SerialName("Intermediate") INTERMEDIATE,
    @SerialName("Advanced") ADVANCED
}

@Serializable
enum class Goal {
    @SerialName("Muscle Gain") MUSCLE_GAIN,
    @SerialName("Weight Loss") WEIGHT_LOSS,
    @SerialName("Endurance") ENDURANCE
}

@Serializable
data class UserProfile(
    val age: Int,
    val weight: Double,
    val fitness_level: FitnessLevel,
    val goal: Goal
)

@Serializable
data class Exercise(
    val exercise_name: String,
    val sets: Int,
    val reps: String,
    val rest_time: String,
    val tutorial_video_url: String,
    val muscle_group: String,
    val intensity: String,
    val calories_per_set: Int,
    val icon: String
)

@Serializable
data class WorkoutDay(
    val day: String,
    val focus: String,
    val exercises: List<Exercise>,
    val estimated_duration_min: Int,
    val total_calories: Int
)

@Serializable
data class WorkoutPlan(
    val plan_name: String,
    val description: String,
    val level: FitnessLevel,
    val goal: Goal,
    val days_per_week: Int,
    val days: List<WorkoutDay>,
    val tips: List<String>,
    val antigravity_mode: Boolean = false
)
