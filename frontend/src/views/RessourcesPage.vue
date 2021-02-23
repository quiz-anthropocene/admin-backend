<template>
  <section class="text-align-left">
    <h2>Ressources pour aller plus loin</h2>

    <section class="alert alert-warning" role="alert" v-if="$i18n.locale === 'en'">
      🌐Page not yet translated ...
    </section>

    <p><i>Table des matières</i></p>
    <ol>
      <li><a href="#ressources-soutiens">Les associations et les personnes qui participent de près ou de loin au projet</a></li>
      <li><a href="#ressources-documentation">Des ressources qui nous ont été utiles pour trouver de nouvelles questions</a></li>
      <li><a href="#ressources-autres-apps">Des projets et jeux similaires</a></li>
      <li><a href="#ressources-autres-liens">D'autres associations et liens qui peuvent vous être utiles</a></li>
      <li><a href="#ressources-glossaire">Un glossaire</a></li>
    </ol>

    <br />
    <h3 id="ressources-soutiens">Les associations et les personnes qui participent de près ou de loin au projet</h3>
    <!-- <a href="https://fresqueduclimat.org/" target="_blank">La Fresque du Climat</a><br />
    <a href="https://avenirclimatique.org/" target="_blank">Avenir Climatique</a><br />
    <a href="http://adrastia.org/" target="_blank">Adrastia</a><br />
    <a href="https://citoyenspourleclimat.org/" target="_blank">Citoyens pour le climat (CPLC)</a><br /> -->

    <p>
      Une variété de profils pour toucher tous les sujets de la crise climatique :
      l'énergie, les ressources, le climat, les questions d'effondrement, les actions possibles, etc
    </p>

    <div v-if="soutiens" id="ressources-soutiens-list" class="row">
      <div class="col-sm-6" v-for="soutien_item in soutiens" :key="soutien_item.name">
        <div class="card">
          <img class="card-img-top" v-bind:src="soutien_item.image_url">
          <div class="card-body">
            <h2 class="card-title"><a v-bind:href="soutien_item.description_url" target="_blank">{{ soutien_item.name }}</a></h2>
            <p class="card-text">
              {{ soutien_item.description }}
            </p>
            <p v-if="soutien_item.description_details">
              🚀&nbsp;{{ soutien_item.description_details }}
            </p>
          </div>
          <div class="card-footer">
            <router-link v-if="soutien_item.quiz_tag" class="no-decoration" :to="{ name: 'quiz-list', query: { tag: soutien_item.quiz_tag } }">
              <a>
                <strong>Tous les quizs </strong>
                <FilterLabel filterType="tag" v-bind:filterValue="soutien_item.quiz_tag"></FilterLabel>
              </a>
            </router-link>
            <router-link v-if="soutien_item.quiz_author" class="no-decoration" :to="{ name: 'quiz-list', query: { author: soutien_item.quiz_author } }">
              <a>
                <strong>Tous les quizs de </strong>
                <FilterLabel filterType="author" v-bind:filterValue="soutien_item.quiz_author"></FilterLabel>
              </a>
            </router-link>
            <router-link v-if="soutien_item.question_author" class="no-decoration" :to="{ name: 'question-list', query: { author: soutien_item.question_author } }">
              <a>
                <strong>Toutes les questions de </strong>
                <FilterLabel filterType="author" v-bind:filterValue="soutien_item.question_author"></FilterLabel>
              </a>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <br />
    <h3 id="ressources-documentation">Des ressources qui nous ont été utiles pour trouver de nouvelles questions</h3>

    <p><i>à venir !</i></p>

    <p>
      Vous trouverez une liste supplémentaire de ressources sur le site
      <a href="https://www.cerise-environnement.com/" target="_blank">CeRISE</a> (Centre de Ressources et d'Informations pour le Secondaire sur l'Environnement).
    </p>

    <br />
    <h3 id="ressources-autres-apps">Des projets et jeux similaires</h3>

    <p>D'autres applications existent pour en apprendre plus sur la crise climatique de manière ludique.</p>

    <div class="card" v-for="autresapps_item in autresApps" :key="autresapps_item.name">
      <div class="row no-gutters">
        <div class="col-2">
          <img v-bind:src="autresapps_item.img_url" class="mr-3" style="max-width: 100%" alt="">
        </div>
        <div class="col-10">
          <div class="card-body">
            <h5 class="mt-0"><a v-bind:href="autresapps_item.description_url" target="_blank">{{ autresapps_item.name }}</a></h5>
            <p>{{ autresapps_item.description }}</p>
          </div>
        </div>
      </div>
      <!-- <div class="media">
        <img v-bind:src="autresapps_item.img_url" class="mr-3" style="width:100px" alt="">
        <div class="media-body">
          <h5 class="mt-0"><a v-bind:href="autresapps_item.description_url" target="_blank">{{ autresapps_item.name }}</a></h5>
          <p>{{ autresapps_item.description }}</p>
        </div>
      </div> -->
    </div>

    <br />
    <h3 id="ressources-autres-liens">D'autres associations et liens qui peuvent vous être utiles</h3>
    <a href="https://theshiftproject.org/" target="_blank">The Shift Project</a><br />
    <a href="https://extinctionrebellion.fr/" target="_blank">Extinction Rebellion (XR)</a><br />
    <a href="https://www.lpo.fr/" target="_blank">La Ligue pour la Protection des Oiseaux (LPO)</a><br />
    <a href="https://www.linkedin.com/company/comment-agir-pour-le-climat/" target="_blank">2 tonnes</a><br />
    <a href="https://cacommenceparmoi.org/" target="_blank">ça commence par moi</a><br />

    <h4>Ca bouge aussi coté politique</h4>
    <a href="https://www.hautconseilclimat.fr/" target="_blank">Le Haut conseil pour le climat</a><br />
    <a href="https://www.conventioncitoyennepourleclimat.fr/" target="_blank">La Convention Citoyenne pour le climat (CCC)</a><br />

    <br />
    <h3 id="ressources-glossaire">Un glossaire</h3>

    <p>
      Voir la page <router-link :to="{ name: 'glossary' }">📓&nbsp;Glossaire</router-link>.
    </p>

  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';
import FilterLabel from '../components/FilterLabel.vue';

export default {
  name: 'RessourcesPage',
  metaInfo() {
    const title = 'Ressources';
    const description = 'Du contenu pour aller plus loin';
    return {
      title,
      meta: metaTagsGenerator(title, description),
    };
  },
  components: {
    FilterLabel,
  },

  mounted() {
    this.$store.dispatch('GET_RESSOURCES_SOUTIENS_LIST_FROM_LOCAL_YAML');
    this.$store.dispatch('GET_RESSOURCES_AUTRES_APPS_LIST_FROM_LOCAL_YAML');
  },

  data() {
    return {
      // soutiens: null,
    };
  },

  computed: {
    soutiens() {
      return this.$store.state.ressources.soutiens;
    },
    autresApps() {
      return this.$store.state.ressources.autresApps;
    },
  },
};
</script>

<style scoped>
.card {
  margin-bottom: 15px;
}
.card-footer > a {
  white-space: nowrap;
  margin-right: 10px;
}
</style>
