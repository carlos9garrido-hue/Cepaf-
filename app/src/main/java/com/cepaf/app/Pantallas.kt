package com.cepaf.app

import android.graphics.BitmapFactory
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.BaselineShift
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// ---------- Estructura común ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun Pantalla(
    titulo: String,
    alVolver: (() -> Unit)? = null,
    acciones: @Composable () -> Unit = {},
    contenido: @Composable (PaddingValues) -> Unit
) {
    Scaffold(
        contentWindowInsets = WindowInsets(0),
        topBar = {
            TopAppBar(
                title = { Text(titulo) },
                navigationIcon = {
                    if (alVolver != null) TextButton(onClick = alVolver) { Text("← Volver") }
                },
                actions = {
                    acciones()
                    if (alVolver == null) MenuTema()
                }
            )
        },
        content = contenido
    )
}

/** Muestra una imagen desde assets/imagenes/<nombre>; si no existe, un recuadro de reserva. */
@Composable
fun ImagenAsset(nombre: String?, modifier: Modifier = Modifier) {
    val ctx = LocalContext.current
    val mapa = remember(nombre) {
        nombre?.let {
            runCatching {
                ctx.assets.open("imagenes/$it").use { s -> BitmapFactory.decodeStream(s)?.asImageBitmap() }
            }.getOrNull()
        }
    }
    if (mapa != null) {
        Image(bitmap = mapa, contentDescription = null, modifier = modifier, contentScale = ContentScale.Crop)
    } else {
        Box(
            modifier.background(MaterialTheme.colorScheme.surfaceVariant),
            contentAlignment = Alignment.Center
        ) { Text("Imagen pendiente", style = MaterialTheme.typography.labelMedium) }
    }
}

// ---------- Evangelio ----------

@Composable
fun ListaCapitulos(alElegir: (Int) -> Unit) {
    Pantalla("Evangelio de San Juan") { p ->
        LazyColumn(Modifier.padding(p)) {
            item {
                Text(
                    "Versión: ${Datos.evangelio.version}",
                    style = MaterialTheme.typography.labelMedium,
                    modifier = Modifier.padding(16.dp)
                )
            }
            items(Datos.evangelio.capitulos) { c ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clickable { alElegir(c.numero) }
                        .padding(horizontal = 16.dp, vertical = 14.dp)
                ) {
                    Text("Capítulo ${c.numero}", style = MaterialTheme.typography.titleMedium)
                    Text("${c.versiculos.size} versículos", style = MaterialTheme.typography.bodySmall)
                }
                HorizontalDivider()
            }
        }
    }
}

@Composable
fun LecturaCapitulo(numero: Int, alVolver: () -> Unit) {
    val capitulo = Datos.evangelio.capitulos.first { it.numero == numero }
    var tam by remember { mutableFloatStateOf(18f) }
    val colorNumero = MaterialTheme.colorScheme.primary

    Pantalla(
        titulo = "Juan $numero",
        alVolver = alVolver,
        acciones = {
            TextButton(onClick = { if (tam > 14f) tam -= 2f }) { Text("A-") }
            TextButton(onClick = { if (tam < 30f) tam += 2f }) { Text("A+") }
        }
    ) { p ->
        LazyColumn(
            Modifier.padding(p),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(capitulo.versiculos) { v ->
                val texto = buildAnnotatedString {
                    withStyle(
                        SpanStyle(
                            fontSize = (tam * 0.7f).sp,
                            fontWeight = FontWeight.Bold,
                            color = colorNumero,
                            baselineShift = BaselineShift.Superscript
                        )
                    ) { append("${v.numero} ") }
                    append(v.texto)
                }
                Text(texto, fontSize = tam.sp, lineHeight = (tam * 1.5f).sp)
            }
        }
    }
}

// ---------- Lectio Divina ----------

@Composable
fun PantallaLectio() {
    Pantalla("Lectio Divina") { p ->
        LazyColumn(
            Modifier.padding(p),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            itemsIndexedPasos()
        }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.itemsIndexedPasos() {
    items(Datos.lectio.size) { i ->
        val paso = Datos.lectio[i]
        Card(
            Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
        ) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("${i + 1}. ${paso.nombre}", style = MaterialTheme.typography.titleMedium)
                Text(paso.latin, style = MaterialTheme.typography.labelMedium)
                Text(paso.descripcion, style = MaterialTheme.typography.bodyMedium)
                paso.preguntas.forEach { Text("• $it", style = MaterialTheme.typography.bodyMedium) }
            }
        }
    }
}

// ---------- Glosario de ciudades ----------

@Composable
fun ListaCiudades(alElegir: (String) -> Unit) {
    Pantalla("Ciudades y lugares") { p ->
        LazyColumn(Modifier.padding(p)) {
            items(Datos.ciudades) { c ->
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clickable { alElegir(c.id) }
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    if (c.imagen != null) {
                        ImagenAsset(c.imagen, Modifier.height(56.dp).fillMaxWidth(0.2f).clip(MaterialTheme.shapes.small))
                    }
                    Column {
                        Text(c.nombre, style = MaterialTheme.typography.titleMedium)
                        Text(c.region, style = MaterialTheme.typography.bodySmall)
                    }
                }
                HorizontalDivider()
            }
        }
    }
}

@Composable
fun DetalleCiudad(id: String, alVolver: () -> Unit) {
    val c = Datos.ciudades.first { it.id == id }
    Pantalla(c.nombre, alVolver) { p ->
        Column(
            Modifier
                .padding(p)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            if (c.imagen != null) {
                ImagenAsset(c.imagen, Modifier.fillMaxWidth().height(180.dp).clip(MaterialTheme.shapes.medium))
            }
            Text(c.region, style = MaterialTheme.typography.labelLarge)
            Text("En San Juan: ${c.referencias}", style = MaterialTheme.typography.bodySmall)
            Text("Historia", style = MaterialTheme.typography.titleMedium)
            Text(c.historia, style = MaterialTheme.typography.bodyLarge)
            Text("Quiénes gobernaban", style = MaterialTheme.typography.titleMedium)
            Text(c.gobierno, style = MaterialTheme.typography.bodyLarge)
        }
    }
}

// ---------- Personajes ----------

@Composable
fun ListaPersonajes(alElegir: (String) -> Unit) {
    Pantalla("Personajes de los signos") { p ->
        LazyColumn(Modifier.padding(p)) {
            items(Datos.personajes) { x ->
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clickable { alElegir(x.id) }
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    ImagenAsset(x.imagen, Modifier.height(56.dp).fillMaxWidth(0.2f).clip(MaterialTheme.shapes.small))
                    Column {
                        Text(x.nombre, style = MaterialTheme.typography.titleMedium)
                        Text("${x.milagro} (${x.referencia})", style = MaterialTheme.typography.bodySmall)
                    }
                }
                HorizontalDivider()
            }
        }
    }
}

@Composable
fun DetallePersonaje(id: String, alVolver: () -> Unit) {
    val x = Datos.personajes.first { it.id == id }
    Pantalla(x.nombre, alVolver) { p ->
        Column(
            Modifier
                .padding(p)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ImagenAsset(x.imagen, Modifier.fillMaxWidth().height(220.dp).clip(MaterialTheme.shapes.medium))
            Text("${x.milagro} — Juan ${x.referencia}", style = MaterialTheme.typography.labelLarge)
            Text(x.biografia, style = MaterialTheme.typography.bodyLarge)
        }
    }
}

// ---------- Folleto ----------

@Composable
fun ListaTemas(alElegir: (Int) -> Unit) {
    Pantalla("Folleto") { p ->
        LazyColumn(Modifier.padding(p)) {
            item {
                Text(
                    Datos.folleto.titulo,
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(16.dp)
                )
            }
            items(Datos.folleto.temas) { t ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .clickable { alElegir(t.numero) }
                        .padding(horizontal = 16.dp, vertical = 14.dp)
                ) {
                    Text("TEMA ${t.numero}", style = MaterialTheme.typography.labelLarge)
                    Text(t.titulo, style = MaterialTheme.typography.titleMedium)
                }
                HorizontalDivider()
            }
        }
    }
}

@Composable
fun LecturaTema(numero: Int, alVolver: () -> Unit) {
    val tema = Datos.folleto.temas.first { it.numero == numero }
    var tam by remember { mutableFloatStateOf(17f) }

    Pantalla(
        titulo = "Tema ${tema.numero}",
        alVolver = alVolver,
        acciones = {
            TextButton(onClick = { if (tam > 14f) tam -= 2f }) { Text("A-") }
            TextButton(onClick = { if (tam < 30f) tam += 2f }) { Text("A+") }
        }
    ) { p ->
        LazyColumn(
            Modifier.padding(p),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                Text(
                    tema.titulo,
                    style = MaterialTheme.typography.headlineSmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            items(tema.bloques) { b ->
                when (b.tipo) {
                    "seccion" -> Text(
                        b.texto.orEmpty(),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.secondary,
                        modifier = Modifier.padding(top = 10.dp)
                    )
                    "caja" -> Card(
                        Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Text(
                            b.texto.orEmpty(),
                            fontSize = tam.sp,
                            lineHeight = (tam * 1.45f).sp,
                            fontStyle = FontStyle.Italic,
                            modifier = Modifier.padding(16.dp)
                        )
                    }
                    "subtitulo" -> Text(
                        b.texto.orEmpty(),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    "lista" -> Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        b.items.forEach { item ->
                            Text(
                                buildAnnotatedString {
                                    append("•  ")
                                    if (item.titulo != null) {
                                        withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(item.titulo + " ") }
                                    }
                                    append(item.texto)
                                },
                                fontSize = tam.sp,
                                lineHeight = (tam * 1.45f).sp
                            )
                        }
                    }
                    else -> Text(
                        b.texto.orEmpty(),
                        fontSize = tam.sp,
                        lineHeight = (tam * 1.45f).sp
                    )
                }
            }
        }
    }
}
