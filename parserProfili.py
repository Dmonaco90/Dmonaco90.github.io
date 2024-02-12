from bs4 import BeautifulSoup
import json

html_input = """
                <div class="measure-section zeta" id="drawSection">
                    <div class="image-container zeta">
                        <img src="static/img/zeta2.png" alt="zeta">
                        <input type="number" class="input-lato lato-zeta" id="lato1-zeta" style="top: 8%; left: 10%;   " placeholder="x">
                        <input type="number" class="input-lato lato-zeta" id="lato2-zeta" style="top: 82%; left: 69%;  " placeholder="x">
                        <input type="number" class="input-lato lato-zeta" id="lato3-zeta" style="top: 47%; right: 52%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta1" style="position: absolute;  margin: 0; width: auto; top: 63%; left: 50%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta2" style="position: absolute;  margin: 0; width: auto; top: 27%; left: 37%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section u" id="drawSection">
                    <div class="image-container u">
                        <img src="static/img/u.png" alt="u">
                        <input type="number" class="input-lato lato-u" id="lato1-u" style="top: 45%; left: 12%;  " placeholder="x">
                        <input type="number" class="input-lato lato-u" id="lato2-u" style="top: 65%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-u" id="lato3-u" style="top: 45%; right: 1%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 47%; left: 30%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 58%; left: 18%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section omega5" id="drawSection">
                    <div class="image-container omega5">
                        <img src="static/img/omega5.png" alt="u">
                        <input type="number" class="input-lato lato-omega5" id="lato1-Omega5" style="top: 25%; left: 25%;  " placeholder="x">
                        <input type="number" class="input-lato lato-omega5" id="lato1-Omega5" style="top: 25%; right: 13%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato2-Omega5" style="top: 75%; left: 47%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 59%; right: 10%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 59%; left: 10%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 64%; right: 23%;   text-align:center;" placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 64%; left: 20%;  text-align:right;" placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 40%; left: -1%;  text-align:right;" placeholder="x">
                        <input type="number" class="input-lato lato-Omega5" id="lato3-Omega5" style="top: 40%; right: -1%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 22%; left: 83%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 35%; left: 69%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section LineaAngolare" id="drawSection">
                    <div class="image-container LineaAngolare">
                        <img src="static/img/LineaAngolare.png" alt="u">
                        <input type="number" class="input-lato lato-LineaAngolare" id="lato1-LineaAngolare" style="top: 43%; right: 29%;  " placeholder="x">
                        <input type="number" class="input-lato lato-LineaAngolare" id="lato2-LineaAngolare" style="top: 48%; left: 42%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna2.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 41%; left: 25%;">
                            <img src="static/img/freccia_esterna2.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 59%; left: 58%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section OmegaAsi2" id="drawSection">
                    <div class="image-container OmegaAsi2">
                        <img src="static/img/OmegaAsi2.png" alt="u">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato1-OmegaAsi2" style="top: 32%; right: 8%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato2-OmegaAsi2" style="top: 43%; right: 22%;  text-align: right;" placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato3-OmegaAsi2" style="top: 69%; right: 0%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato1-OmegaAsi2" style="top: 68%; left: 9%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato2-OmegaAsi2" style="top: 83%; left: 47%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato3-OmegaAsi2" style="top: 55%; right: 18%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi2" id="lato3-OmegaAsi2" style="top: 18%; right: 9%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna2.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 65%; left: 25%;">
                            <img src="static/img/freccia_esterna2.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 81%; left: 58%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section L" id="drawSection">
                    <div class="image-container L">
                        <img src="static/img/L.png" alt="L">

                        <input type="number" class="input-lato lato-L" id="lato2-L" style="top: 50%; left: 6%;  " placeholder="x">
                        <input type="number" class="input-lato lato-L" id="lato3-L" style="top: 75%; right: 35%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta111" style="position: absolute;  margin: 0; width: auto; top: 46%; left: 31%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta222" style="position: absolute;  margin: 0; width: auto; top: 57%; left: 19%;">
                        </div>

                    </div>
                </div>

                <div class="measure-section Linea" id="drawSection">
                    <div class="image-container Linea">
                        <img src="static/img/Linea.png" alt="Linea">

                        <input type="number" class="input-lato lato-Linea" id="lato2-Linea" style="top: 40%; left: 50%;  " placeholder="x">

                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section omega" id="drawSection">
                    <div class="image-container omega">
                        <img src="static/img/omega.png" alt="omega">
                        <input type="number" class="input-lato lato-omega" id="lato1-omega" style="top: 20%; left: 10%;  " placeholder="x">
                        <input type="number" class="input-lato lato-omega" id="lato2-omega" style="top: 75%; left: 52%;  " placeholder="x">
                        <input type="number" class="input-lato lato-omega" id="lato3-omega" style="top: 20%; right: 5%;  " placeholder="x">
                        <input type="number" class="input-lato lato-omega" id="lato4-omega" style="top: 50%; right: 7%;  " placeholder="x">
                        <input type="number" class="input-lato lato-omega" id="lato5-omega" style="top: 50%; left: 22%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 52%; left: 35%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 64%; left: 22%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section OmegaAsi" id="drawSection">
                    <div class="image-container OmegaAsi">
                        <img src="static/img/OmegaAsi.png" alt="u">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato1-OmegaAsi" style="top: 12%; left: 38%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato2-OmegaAsi" style="top: 80%; left: 38%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato3-OmegaAsi" style="top: 61%; right: 1%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato4-OmegaAsi" style="top: 47%; left: 15%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato5-OmegaAsi" style="top: 61%; left: 54%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaAsi" id="lato6-OmegaAsi" style="top: 30%; right: 30%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 56%; left: 38%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 68%; left: 26%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section OmegaInt" id="drawSection">
                    <div class="image-container OmegaInt">
                        <img src="static/img/OmegaInt.png" alt="OmegaInt">
                        <input type="number" class="input-lato lato-OmegaInt" id="lato1-OmegaInt" style="top: 25%; left: 20%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaInt" id="lato2-OmegaInt" style="top: 80%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaInt" id="lato3-OmegaInt" style="top: 25%; right: 15%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaInt" id="lato4-OmegaInt" style="top: 50%; right: -1%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaInt" id="lato5-OmegaInt" style="top: 50%; left: 3%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 56%; left: 27%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 67%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section OmegaIntAsi" id="drawSection">
                    <div class="image-container OmegaIntAsi">
                        <img src="static/img/OmegaIntAsi.png" alt="OmegaIntAsi">
                        <input type="number" class="input-lato lato-OmegaIntAsi" id="lato1-OmegaIntAsi" style="top: 17%; left: 35%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaIntAsi" id="lato2-OmegaIntAsi" style="top: 80%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaIntAsi" id="lato3-OmegaIntAsi" style="top: 34%; right: 15%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaIntAsi" id="lato4-OmegaIntAsi" style="top: 50%; right: -1%;  " placeholder="x">
                        <input type="number" class="input-lato lato-OmegaIntAsi" id="lato5-OmegaIntAsi" style="top: 50%; left: 3%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 56%; left: 27%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 67%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section Scatola" id="drawSection">
                    <div class="image-container Scatola">
                        <img src="static/img/Scatola.png" alt="Scatola">
                        <input type="number" class="input-lato lato-Scatola" id="lato1-Scatola" style="top: 63%; left: 5%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Scatola" id="lato2-Scatola" style="top: 81%; left: 34%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Scatola" id="lato3-Scatola" style="top: 69%; left: 67%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Scatola" id="lato4-Scatola" style="top: 56%; right: 3%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Scatola" id="lato5-Scatola" style="top: 24%; right: -6%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Scatola" id="lato5-Scatola" style="top: 24%; left: 23%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 72%; left: 27%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 81%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section Amo" id="drawSection">
                    <div class="image-container Amo">
                        <img src="static/img/Amo.png" alt="Amo">
                        <input type="number" class="input-lato lato-Amo" id="lato1-Amo" style="top: 32%; left: 15%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Amo" id="lato2-Amo" style="top: 65%; left: 50%;  " placeholder="x">
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 44%; left: 34%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 55%; left: 24%;">
                        </div>
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                    </div>
                </div>

                <div class="measure-section Ami" id="drawSection">
                    <div class="image-container Ami">
                        <img src="static/img/Ami.png" alt="Ami">
                        <input type="number" class="input-lato lato-Ami" id="lato1-Ami" style="top: 32%; left: 22%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Ami" id="lato2-Ami" style="top: 60%; left: 48%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Ami" id="lato3-Ami" style="top: 32%; right: 18%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna2.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 41%; left: 36%;">
                            <img src="static/img/freccia_esterna2.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 57%; left: 51%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section gancio" id="drawSection">
                    <div class="image-container gancio">
                        <img src="static/img/gancio.png" alt="gancio">
                        <input type="number" class="input-lato lato-gancio" id="lato1-gancio" style="top: 28%; left: 30%;  " placeholder="x">
                        <input type="number" class="input-lato lato-gancio" id="lato2-gancio" style="top: 70%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-gancio" id="lato3-gancio" style="top: 50%; left: 15%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 46%; left: 32%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 58%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section P_rovescia" id="drawSection">
                    <div class="image-container P_rovescia">
                        <img src="static/img/P_rovescia.png" alt="P_rovescia">
                        <input type="number" class="input-lato lato-P_rovescia" id="lato1-P_rovescia" style="top: 32%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P_rovescia" id="lato2-P_rovescia" style="top: 69%; left: 61%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P_rovescia" id="lato3-P_rovescia" style="top: 43%; left: 25%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P_rovescia" id="lato4-P_rovescia" style="top: 50%; left: 70%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 31%; left: 68%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 43%; left: 55%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section P" id="drawSection">
                    <div class="image-container P">
                        <img src="static/img/P.png" alt="P">
                        <input type="number" class="input-lato lato-P" id="lato1-P" style="top: 25%; left: 37%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P" id="lato2-P" style="top: 61%; left: 45%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P" id="lato3-P" style="top: 43%; left: 24%;  " placeholder="x">
                        <input type="number" class="input-lato lato-P" id="lato3-P" style="top: 34%; left: 47%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 46%; left: 32%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 58%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section Freccia" id="drawSection">
                    <div class="image-container Freccia">
                        <img src="static/img/Freccia.png" alt="Freccia">

                        <input type="number" class="input-lato lato-Freccia" id="lato2-Freccia" style="top: 62%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Freccia" id="lato3-Freccia" style="top: 44%; left: 20%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 46%; left: 32%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 58%; left: 16%;">
                        </div>
                    </div>
                </div>

                <div class="measure-section L45" id="drawSection">
                    <div class="image-container L45">
                        <img src="static/img/L45.png" alt="L45">
                    
                        <input type="number" class="input-lato lato-Freccia" id="lato2-Freccia" style="top: 62%; left: 50%;  " placeholder="x">
                        <input type="number" class="input-lato lato-Freccia" id="lato3-Freccia" style="top: 44%; left: 20%;  " placeholder="x">
                        <!-- Aggiungi altri input box come necessario, posizionandoli con lo stile inline -->
                        <div class="scelteVerniciato" style="display: none;">
                            <img src="static/img/freccia_interna.png" class="opzioneVerniciato" id="scelta11" style="position: absolute;  margin: 0; width: auto; top: 46%; left: 32%;">
                            <img src="static/img/freccia_esterna.png" class="opzioneVerniciato" id="scelta21" style="position: absolute;  margin: 0; width: auto; top: 58%; left: 16%;">
                        </div>
                    </div>
                </div>
                """
                
                
scalature = {
    "omega": {
        "6/10": 6, "8/10": 6, "10/10": 6, "12/10": 6,
        "15/10": 7, "20/10": 10, "30/10": 16,
    },
    "zeta": {
        "6/10": 3, "8/10": 3, "10/10": 3, "12/10": 3, "15/10": 3,
        "20/10": 4, "30/10": 6,
    },
    "Ami": {
        "6/10": 3, "8/10": 3, "10/10": 3, "12/10": 3,
        "15/10": 6, "20/10": 5, "30/10": 8,
    },
    "OmegaInt": {
        "6/10": 8, "8/10": 8, "10/10": 8, "12/10": 8,
        "15/10": 10, "20/10": 14, "30/10": 21,
    },
    "OmegaIntAsi": {
        "6/10": 8, "8/10": 8, "10/10": 8, "12/10": 8,
        "15/10": 10, "20/10": 14, "30/10": 21,
    },
    "L": {
        "6/10": 2, "8/10": 2, "10/10": 2, "12/10": 2, "15/10": 2,
        "20/10": 3, "30/10": 5,
    },
    "omega5": {
        "6/10": 12, "8/10": 12, "10/10": 12, "12/10": 12,
        "15/10": 14, "20/10": 20, "30/10": 31,
    },
    "OmegaAsi": {
        "6/10": 8, "8/10": 8, "10/10": 8, "12/10": 8,
        "15/10": 12, "20/10": 16, "30/10": 20,
    },
    "OmegaAsi2": {
        "6/10": 8, "8/10": 8, "10/10": 8, "12/10": 8, "15/10": 8,
        "20/10": 11, "30/10": 19,
    },
    "Amo": {
        "6/10": 1, "8/10": 1, "10/10": 1, "12/10": 1, "15/10": 1,
        "20/10": 0, "30/10": 3,
    },
    "gancio": {
        "6/10": 4, "8/10": 4, "10/10": 4, "12/10": 4,
        "15/10": 5, "20/10": 7, "30/10": 11,
    },
    "u": {
        "6/10": 4, "8/10": 4, "10/10": 4, "12/10": 4,
        "15/10": 5, "20/10": 7, "30/10": 11,
    },
    "Scatola": {
        "6/10": 4, "8/10": 4, "10/10": 4, "12/10": 4,
        "15/10": 5, "20/10": 7, "30/10": 11,
    },
    "Freccia": {
        "6/10": 2, "8/10": 2, "10/10": 2, "12/10": 2, "15/10": 2,
        "20/10": 3, "30/10": 5,
    },
    "L45": {
        "6/10": 2, "8/10": 2, "10/10": 2, "12/10": 2, "15/10": 2,
        "20/10": 3, "30/10": 5,
    },
    "P": {
            "6/10": 6, "8/10": 6, "10/10": 6, "12/10": 6,
            "15/10": 7, "20/10": 10, "30/10": 16,
        },
    "P_rovescia": {
            "6/10": 6, "8/10": 6, "10/10": 6, "12/10": 6,
            "15/10": 7, "20/10": 10, "30/10": 16,
        }               
}


soup = BeautifulSoup(html_input, 'html.parser')
profiles = []

# Process each measure-section
for section in soup.find_all("div", class_="measure-section"):
    profile_name = section.get("class")[1]  # Get the profile name
    image_url = section.find("img").get("src")
    input_boxes = []
    vern_boxes = []

    # Process each input
    for input_tag in section.find_all("input"):
        input_boxes.append({
            "id": input_tag.get("id"),
            "top": input_tag.get("style").split(";")[0].split(":")[1].strip(),
            "left": input_tag.get("style").split(";")[1].split(":")[1].strip(),
            "placeholder": input_tag.get("placeholder")
        })

    # Process each verniciato option
    for img in section.find_all("img", class_="opzioneVerniciato"):
        vern_boxes.append({
            "id": img.get("id"),
            "top": img.get("style").split(";")[3].split(":")[1].strip() if len(img.get("style").split(";")) > 3 else "auto",
            "left": img.get("style").split(";")[4].split(":")[1].strip() if len(img.get("style").split(";")) > 4 else img.get("style").split(";")[2].split(":")[1].strip(),
            "url": img.get("src")
        })

    # Append the profile data to the profiles list
    profiles.append({
        "id": profile_name,
        "imageUrl": image_url,
        "inputBoxes": input_boxes,
        "vernBoxes": vern_boxes
    })

for profile in profiles:
    profile_id = profile["id"]
    if profile_id in scalature:
        profile["scalature"] = scalature[profile_id]

# Convert the 'full_profiles' list to a JSON formatted string
json_output = json.dumps(profiles, indent=4)

# Save the JSON output to a file
file_path = 'profiles.json'
with open(file_path, 'w') as file:
    file.write(json_output)