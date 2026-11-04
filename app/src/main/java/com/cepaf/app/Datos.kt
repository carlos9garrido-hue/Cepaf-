package com.cepaf.app

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

data class Versiculo(val numero: Int, val texto: String)
data class Capitulo(val numero: Int, val versiculos: List<Versiculo>)
data class Evangelio(val version: String, val capitulos: List<Capitulo>)

data class Ciudad(
    val id: String,
    val nombre: String,
    val region: String,
    val referencias: String,
    val historia: String,
    val gobierno: String,
    val imagen: String?
)

data class Personaje(
    val id: String,
    val nombre: String,
    val milagro: String,
    val referencia: String,
    val biografia: String,
    val imagen: String?
)

data class PasoLectio(
    val nombre: String,
    val latin: String,
    val descripcion: String,
    val preguntas: List<String>
)

/** Carga los contenidos desde la carpeta assets (archivos JSON editables). */
object Datos {
    lateinit var evangelio: Evangelio
    lateinit var ciudades: List<Ciudad>
    lateinit var personajes: List<Personaje>
    lateinit var lectio: List<PasoLectio>

    fun cargar(ctx: Context) {
        val juan = JSONObject(leer(ctx, "juan.json"))
        evangelio = Evangelio(
            version = juan.getString("version"),
            capitulos = juan.getJSONArray("capitulos").objetos().map { c ->
                Capitulo(
                    numero = c.getInt("numero"),
                    versiculos = c.getJSONArray("versiculos").objetos().map {
                        Versiculo(it.getInt("n"), it.getString("t"))
                    }
                )
            }
        )
        ciudades = JSONArray(leer(ctx, "glosario.json")).objetos().map {
            Ciudad(
                it.getString("id"), it.getString("nombre"), it.getString("region"),
                it.getString("referencias"), it.getString("historia"),
                it.getString("gobierno"), it.optString("imagen").ifBlank { null }
            )
        }
        personajes = JSONArray(leer(ctx, "personajes.json")).objetos().map {
            Personaje(
                it.getString("id"), it.getString("nombre"), it.getString("milagro"),
                it.getString("referencia"), it.getString("biografia"),
                it.optString("imagen").ifBlank { null }
            )
        }
        lectio = JSONArray(leer(ctx, "lectio.json")).objetos().map { p ->
            PasoLectio(
                p.getString("nombre"), p.getString("latin"), p.getString("descripcion"),
                p.getJSONArray("preguntas").let { a -> (0 until a.length()).map { a.getString(it) } }
            )
        }
    }

    private fun leer(ctx: Context, nombre: String): String =
        ctx.assets.open(nombre).bufferedReader(Charsets.UTF_8).use { it.readText() }

    private fun JSONArray.objetos(): List<JSONObject> =
        (0 until length()).map { getJSONObject(it) }
}
