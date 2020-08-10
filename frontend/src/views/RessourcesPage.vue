<template>

  <section class="text-align-left">
    <h2>Ressources pour aller plus loin</h2>

    <h3>Les associations et les personnes qui participent de près ou de loin au projet</h3>
    <!-- <a href="https://fresqueduclimat.org/" target="_blank">La Fresque du Climat</a><br />
    <a href="https://avenirclimatique.org/" target="_blank">Avenir Climatique</a><br />
    <a href="http://adrastia.org/" target="_blank">Adrastia</a><br />
    <a href="https://citoyenspourleclimat.org/" target="_blank">Citoyens pour le climat (CPLC)</a><br /> -->

    <p>
      Une variété de profils pour toucher tous les sujets de la crise climatique :
      l'énergie, les ressources, le climat, les questions d'effondrement, les actions possibles, etc
    </p>

    <div class="row">
      <div class="col-sm-6" v-for="soutien_item in soutiens" :key="soutien_item.name">
        <div class="card">
          <img class="card-img-top" v-bind:src="soutien_item.image_url">
          <div class="card-body">
            <h2 class="card-title">{{ soutien_item.name }}</h2>
            <p class="card-text">
              {{ soutien_item.description }}
              <a v-bind:href="soutien_item.description_url" target="_blank">lien</a>
            </p>
            <p v-if="soutien_item.description_details">
              🚀&nbsp;{{ soutien_item.description_details }}
            </p>
          </div>
          <div class="card-footer" v-if="soutien_item.quiz_tag">
            <router-link class="no-decoration" :to="{ name: 'quiz-list', query: { tag: soutien_item.quiz_tag.name } }">
              <a>Voir les quizs : <FilterLabel filterType="tag" v-bind:filterObject="{ name: soutien_item.quiz_tag.name }"></FilterLabel></a>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <br />
    <h3>Des ressources qui nous ont été utiles pour trouver de nouvelles questions</h3>

    <p>à venir</p>

    <br />
    <h3>Des projets et jeux similaires</h3>

    <p>à venir</p>

    <br />
    <h3>D'autres associations et liens qui peuvent vous être utiles</h3>
    <a href="https://theshiftproject.org/" target="_blank">The Shift Project</a><br />
    <a href="https://extinctionrebellion.fr/" target="_blank">Extinction Rebellion (XR)</a><br />
    <a href="https://www.lpo.fr/" target="_blank">La Ligue pour la Protection des Oiseaux (LPO)</a><br />
    <a href="https://www.linkedin.com/company/comment-agir-pour-le-climat/" target="_blank">2 tonnes</a><br />
    <a href="https://cacommenceparmoi.org/" target="_blank">ça commence par moi</a><br />
    <a href="https://www.hautconseilclimat.fr/" target="_blank">Le Haut conseil pour le climat</a><br />
    <a href="https://www.conventioncitoyennepourleclimat.fr/" target="_blank">La Convention Citoyenne pour le climat (CCC)</a><br />

  </section>
</template>

<script>
import FilterLabel from '../components/FilterLabel.vue';

export default {
  name: 'RessourcesPage',
  metaInfo: {
    title: 'Ressources',
    meta: [
      { property: 'og:title', vmid: 'og:title', content: 'Ressources' },
      { property: 'twitter:title', vmid: 'twitter:title', content: 'Ressources' },
    ],
  },
  components: {
    FilterLabel,
  },

  mounted() {
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
  },
};
</script>

<style scoped>
.row > .col-sm-6 {
  padding-bottom: 15px;
}

.card-img-top {
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}
</style>
