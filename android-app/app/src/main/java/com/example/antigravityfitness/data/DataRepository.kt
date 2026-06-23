package com.example.antigravityfitness.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody

interface DataRepository {
  suspend fun generateWorkoutPlan(profile: UserProfile): WorkoutPlan
}

class DefaultDataRepository : DataRepository {
  private val client = OkHttpClient()
  private val json = Json { ignoreUnknownKeys = true }
  
  // Bilgisayarın yerel ağ IP adresi (Fiziksel cihazlar ve emülatörler için ortak)
  // Emülatör kullanıyorsanız: 10.0.2.2
  // Fiziksel cihaz kullanıyorsanız: Kendi Wi-Fi IP adresinizi yazın (örn: 192.168.x.x)
  private val baseUrl = "http://192.168.1.3:8000/api"

  override suspend fun generateWorkoutPlan(profile: UserProfile): WorkoutPlan = withContext(Dispatchers.IO) {
    val jsonBody = json.encodeToString(profile)
    val mediaType = "application/json; charset=utf-8".toMediaType()
    val requestBody = jsonBody.toRequestBody(mediaType)

    val request = Request.Builder()
      .url("$baseUrl/generate")
      .post(requestBody)
      .build()

    client.newCall(request).execute().use { response ->
      if (!response.isSuccessful) {
        throw Exception("Sunucu Hatası: ${response.code}")
      }
      val responseBody = response.body?.string() ?: throw Exception("Boş yanıt alındı")
      json.decodeFromString<WorkoutPlan>(responseBody)
    }
  }
}
