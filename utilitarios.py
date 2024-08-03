from math import ceil
def serializadorPaginacion(total:int,pagina:int,porPagina:int):
    itemsPorPagina = porPagina if total >= porPagina else total

    totalPaginas = ceil(total/itemsPorPagina) if itemsPorPagina > 0 else None
    paginaPrevia = pagina-1 if pagina>1 and pagina<=totalPaginas else None
    paginaSiguiente = pagina+1 if totalPaginas > 1 and pagina<totalPaginas else None

    return {
        "itemsPorPagina":itemsPorPagina,
        "totalPaginas":totalPaginas,
        "total":total,
        "paginaPrevia":paginaPrevia,
        "paginaSiguiente":paginaSiguiente,
        "porPagina": porPagina,
        "pagina":pagina
    }