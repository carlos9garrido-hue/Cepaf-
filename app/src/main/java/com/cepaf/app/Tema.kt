package com.cepaf.app

import android.content.Context
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

/** Ajuste de tema guardado en el dispositivo: 0 = predeterminado (sistema), 1 = claro, 2 = oscuro. */
object Ajustes {
    var modo by mutableIntStateOf(0)
        private set

    private const val ARCHIVO = "ajustes"
    private const val CLAVE = "tema"

    fun cargar(ctx: Context) {
        modo = ctx.getSharedPreferences(ARCHIVO, Context.MODE_PRIVATE).getInt(CLAVE, 0)
    }

    fun cambiar(ctx: Context, nuevo: Int) {
        modo = nuevo
        ctx.getSharedPreferences(ARCHIVO, Context.MODE_PRIVATE).edit().putInt(CLAVE, nuevo).apply()
    }
}

private val EsquemaClaro = lightColorScheme(
    primary = Color(0xFF7B1E2B),
    secondary = Color(0xFF8A6D3B),
    surfaceVariant = Color(0xFFF1E9DC),
    background = Color(0xFFFFFBF5),
    surface = Color(0xFFFFFBF5)
)

private val EsquemaOscuro = darkColorScheme(
    primary = Color(0xFFE6A5AF),
    onPrimary = Color(0xFF3A0A12),
    secondary = Color(0xFFD9BC85),
    background = Color(0xFF181314),
    onBackground = Color(0xFFEDE0E2),
    surface = Color(0xFF181314),
    onSurface = Color(0xFFEDE0E2),
    surfaceVariant = Color(0xFF2C2326),
    onSurfaceVariant = Color(0xFFD8C8CB)
)

@Composable
fun TemaCePaF(contenido: @Composable () -> Unit) {
    val oscuro = when (Ajustes.modo) {
        1 -> false
        2 -> true
        else -> isSystemInDarkTheme()
    }
    MaterialTheme(
        colorScheme = if (oscuro) EsquemaOscuro else EsquemaClaro,
        content = contenido
    )
}

/** Botón "Tema" con menú para elegir predeterminado, claro u oscuro. */
@Composable
fun MenuTema() {
    val ctx = LocalContext.current
    var abierto by remember { mutableStateOf(false) }
    Box {
        TextButton(onClick = { abierto = true }) { Text("Tema") }
        DropdownMenu(expanded = abierto, onDismissRequest = { abierto = false }) {
            listOf("Predeterminado", "Claro", "Oscuro").forEachIndexed { i, nombre ->
                DropdownMenuItem(
                    text = { Text(if (Ajustes.modo == i) "✓ $nombre" else nombre) },
                    onClick = {
                        Ajustes.cambiar(ctx, i)
                        abierto = false
                    }
                )
            }
        }
    }
}
