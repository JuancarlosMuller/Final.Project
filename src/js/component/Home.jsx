import React from 'react'
import Post from './Post';

const Home = () => {


    return (
        <div className="container-fluid">
            <div class="container border-top border-muted my-5">
                <div class="card mb-3 border-0 pt-5" style={{ width: "420px" }}>
                    <div class="row g-0">
                        <div class="col-md-4">
                            <img src="https://img.freepik.com/iconos-gratis/usuario_318-875902.jpg" class="img-fluid rounded-circle" alt="Avatar del usuario" />
                        </div>
                        <div class="col-md-8 d-flex align-items-end">
                            <div class="card-body">
                                <h5 class="card-title">Nombre usuario</h5>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card-group my-5">
                    <div class="card">
                        <img style={{ height: "420px" }} src="https://bitwares.net/wp-content/uploads/2021/08/Shooters-Gratuitos-Competitivos-Bitwares-735x400.jpg?crop=1" class="card-img-top" alt="Imagen de referencia grupo" />
                        <div class="card-body d-grid bg-dark">
                        <button type="btn" class="btn btn-dark">¡Shooter!</button>
                        </div>
                    </div>
                    <div class="card">
                        <img style={{ height: "420px" }} src="https://areajugones.sport.es/wp-content/uploads/2020/06/Top-Moba.jpg.webp" class="card-img-top" alt="Imagen de referencia" />
                        <div class="card-body d-grid bg-dark">
                        <button type="btn" class="btn btn-dark mx-2">¡MOBA!</button>
                        </div>
                    </div>
                    <div class="card">
                        <img style={{ height: "420px" }} src="https://c4.wallpaperflare.com/wallpaper/606/502/422/video-game-collage-blizzard-entertainment-diablo-wallpaper-preview.jpg" class="card-img-top" alt="Imagen de referencia" />
                        <div class="card-body d-grid bg-dark">
                        <button type="btn" class="btn btn-dark mx-2">¡MMORPG!</button>
                        </div>
                    </div>
                </div>
                <>
                <Post/>
                </>
            </div>
        </div>


    )
}

export default Home
