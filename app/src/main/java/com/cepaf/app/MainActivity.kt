package com.cepaf.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.sp
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Datos.cargar(applicationContext)
        Ajustes.cargar(applicationContext)
        setContent {
            TemaCePaF {
                CePaFApp()
            }
        }
    }
}

@Composable
fun CePaFApp() {
    val nav = rememberNavController()
    val entrada by nav.currentBackStackEntryAsState()
    val ruta = entrada?.destination?.route ?: "bienvenida"
    val pestanas = listOf(
        "bienvenida" to "Bienvenida",
        "folleto" to "Folleto",
        "personajes" to "Personajes",
        "glosario" to "Ciudades",
        "evangelio" to "Evangelio"
    )

    Scaffold(
        bottomBar = {
            NavigationBar {
                pestanas.forEach { (destino, titulo) ->
                    NavigationBarItem(
                        selected = ruta.substringBefore("/") == destino,
                        onClick = {
                            nav.navigate(destino) {
                                popUpTo("bienvenida") { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        icon = {},
                        label = { Text(titulo, maxLines = 1, fontSize = 11.sp) }
                    )
                }
            }
        }
    ) { relleno ->
        NavHost(nav, startDestination = "bienvenida", modifier = Modifier.padding(relleno)) {
            composable("bienvenida") {
                PantallaBienvenida { nav.navigate("lectio") }
            }
            composable("evangelio") {
                ListaCapitulos { nav.navigate("evangelio/$it") }
            }
            composable(
                "evangelio/{cap}",
                arguments = listOf(navArgument("cap") { type = NavType.IntType })
            ) {
                LecturaCapitulo(it.arguments!!.getInt("cap")) { nav.popBackStack() }
            }
            composable("lectio") { PantallaLectio() }
            composable("glosario") {
                ListaCiudades { nav.navigate("glosario/$it") }
            }
            composable(
                "glosario/{id}",
                arguments = listOf(navArgument("id") { type = NavType.StringType })
            ) {
                DetalleCiudad(it.arguments!!.getString("id")!!) { nav.popBackStack() }
            }
            composable("personajes") {
                ListaPersonajes { nav.navigate("personajes/$it") }
            }
            composable(
                "personajes/{id}",
                arguments = listOf(navArgument("id") { type = NavType.StringType })
            ) {
                DetallePersonaje(it.arguments!!.getString("id")!!) { nav.popBackStack() }
            }
            composable("folleto") {
                ListaTemas { nav.navigate("folleto/$it") }
            }
            composable(
                "folleto/{tema}",
                arguments = listOf(navArgument("tema") { type = NavType.IntType })
            ) {
                LecturaTema(it.arguments!!.getInt("tema")) { nav.popBackStack() }
            }
        }
    }
}
