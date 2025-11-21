# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.1.0] - 2025-01-XX

### ✨ Nuevas Características

#### Sistema de Búsqueda Avanzado
- Implementación de búsqueda unificada que consulta múltiples campos:
  - Nombres de productos
  - Descripciones
  - Categorías
  - Marcas
  - SKUs
- Búsqueda disponible en navegación desktop y móvil
- Búsqueda en tiempo real con resultados instantáneos

#### Sistema de Filtrado Completo
- **Filtros implementados:**
  - Por categorías (selección múltiple)
  - Por marcas (selección múltiple)
  - Por rango de precios (mínimo/máximo)
  - Opciones especiales: productos en oferta, destacados, con stock
  
- **Características del filtrado:**
  - Filtros colapsables con acordeón
  - Submit automático en checkboxes
  - Preservación de filtros activos durante navegación
  - Visualización de filtros activos con badges
  - Opción para limpiar filtros individuales o todos
  - Sidebar sticky en desktop
  - Modal fullscreen en móvil

#### Sistema de Categorías
- Nueva página de listado de categorías (`category_list.html`)
  - Grid con tarjetas visuales
  - Iconos específicos por tipo de categoría
  - Contador de productos por categoría
- Página de detalle de categoría (`category_detail.html`)
  - Sistema completo de filtrado
  - Ordenamiento de productos
  - Paginación integrada
  - Breadcrumbs de navegación

#### Sistema de Paginación
- Navegación completa: Primera | Anterior | Actual | Siguiente | Última
- Configuración de 12 productos por página
- Información detallada de resultados (Ej: "Mostrando 1-12 de 50 productos")
- Preservación automática de todos los parámetros:
  - Query de búsqueda
  - Filtros de categoría y marca
  - Rangos de precio
  - Opciones especiales
  - Orden de clasificación
- Manejo de errores para páginas fuera de rango

### 🎨 Mejoras de UI/UX

#### Experiencia Móvil
- Modal de filtros para dispositivos móviles
  - Botón flotante para acceder a filtros
  - Modal fullscreen en dispositivos pequeños
  - Misma funcionalidad que versión desktop
- Diseño responsive mejorado:
  - Grid adaptativo: 2 columnas (móvil) → 3 (tablet) → 4 (desktop)
  - Sidebar de filtros oculto en móvil, visible en desktop
  - Barra de búsqueda adaptada para móvil
  - Menú hamburguesa reorganizado con separadores

#### Navegación
- Navbar reorganizada:
  - Barra de búsqueda integrada en desktop
  - Menú móvil mejorado con separadores visuales
  - Opciones de usuario mejor organizadas
  - Búsqueda visible en móvil
- Breadcrumbs implementados en todas las páginas relevantes
- Navegación jerárquica clara

#### Filtros y Controles
- Diseño más limpio con colapsables
- Checkboxes personalizados con mejor feedback visual
- Switches para opciones especiales
- Indicadores visuales de filtros activos
- Contador de filtros activos por sección

#### Visualización de Productos
- Mejor visualización de stock
- Badges más informativos
- Diseño de cards más consistente
- Mejor manejo de imágenes placeholder

### ⚡ Optimizaciones

#### Base de Datos
- Uso de `select_related()` para categorías y marcas
- Uso de `distinct()` para evitar duplicados en resultados
- Agregaciones con `Count()` para estadísticas de categorías
- Agregaciones con `Min/Max()` para rangos de precios

#### Rendimiento
- Carga optimizada de productos con paginación
- Consultas más eficientes con prefetch de relaciones
- Reducción de queries redundantes

### 🎨 Nuevos Archivos CSS

#### `products.css`
- Estilos para sidebar de filtros
- Checkboxes personalizados
- Switches para opciones especiales
- Cards de productos mejoradas
- Estilos responsive para grid de productos
- Modal de filtros móvil
- Paginación estilizada

#### Modificaciones en CSS existente
- `base.css`: Mejoras en navbar responsive
- Mejor organización de estilos móvil/desktop
- Variables CSS para consistencia de colores

### 📝 Nuevas Vistas y URLs

#### Vistas
- `product_list`: Lógica de filtrado múltiple y paginación implementada
- `category_detail`: Nueva vista con filtrado completo y paginación
- `category_list`: Nueva vista para mostrar todas las categorías

#### URLs
- `/categorias/` - Listado de todas las categorías
- `/categorias/<slug>/` - Detalle de categoría con productos filtrados
- Parámetros GET extendidos para filtros y paginación

### 📄 Nuevos Templates

- `templates/products/category_list.html` - Grid de categorías
- `templates/products/category_detail.html` - Detalle de categoría con filtros
- Modal de filtros móvil en `product_list.html`

### 🔧 Cambios Técnicos

#### Models
- Sin cambios en modelos existentes

#### Views
- Refactorización de `product_list` para incluir lógica de filtrado
- Nueva implementación de paginación con preservación de parámetros
- Nuevas vistas para sistema de categorías

#### Templates
- Refactorización de `product_list.html` con sistema de filtros
- Nuevo sistema de paginación en templates
- Implementación de breadcrumbs
- Modal de filtros para móvil

### 📚 Documentación

- README.md actualizado con nueva estructura del proyecto
- README.md actualizado con nuevas características
- CHANGELOG.md creado para seguimiento de versiones
- Actualización de referencias a repositorio

---

## [1.0.0] - 2025-01-XX

### ✨ Versión Inicial

#### Funcionalidades Base
- Sistema de productos con categorías y marcas
- Carrito de compras con gestión de sesiones
- Sistema de pedidos completo
- Autenticación y perfiles de usuario
- Panel administrativo de Django personalizado

#### Modelos Implementados
- **Products App:**
  - Product (nombre, precio, stock, imagen, SKU, etc.)
  - Category (categorías de productos)
  - Brand (marcas de productos)
  
- **Orders App:**
  - Order (pedidos de clientes)
  - OrderItem (items individuales del pedido)
  
- **Users App:**
  - CustomerProfile (perfil extendido de usuario)

#### Templates y Diseño
- Template base con Bootstrap 5
- Páginas de productos (lista y detalle)
- Carrito de compras
- Proceso de checkout
- Páginas de perfil de usuario
- Sistema de autenticación (login/registro)

#### Características de Administración
- CRUD completo de productos
- Gestión de inventario
- Gestión de pedidos con estados
- Administración de usuarios y perfiles
- Inline editing de OrderItems
- Autocompletado en selecciones

#### UI/UX
- Diseño responsive básico
- Sistema de mensajes Django
- Formato de precios en CLP
- Badges de descuento
- Indicadores de stock

#### Deployment
- Configuración para Render
- Whitenoise para archivos estáticos
- SQLite para desarrollo
- Script de población de base de datos

---

## Tipos de Cambios

- **✨ Nuevas Características** - `Added` para nuevas funcionalidades
- **🔧 Cambios** - `Changed` para cambios en funcionalidades existentes
- **⚠️ Deprecado** - `Deprecated` para funcionalidades que serán eliminadas
- **🗑️ Eliminado** - `Removed` para funcionalidades eliminadas
- **🐛 Correcciones** - `Fixed` para corrección de bugs
- **🔒 Seguridad** - `Security` para vulnerabilidades

## Enlaces

- [Repositorio en GitHub](https://github.com/carandab/GoWest-PetShop)
- [Sitio en Producción](https://gowest-petshop.onrender.com/)

---

**Notas:**
- Las versiones siguen el formato MAJOR.MINOR.PATCH
- Las fechas están en formato YYYY-MM-DD
- Los cambios se organizan por categorías para mejor legibilidad
