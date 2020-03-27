<template>
  <section class="text-align-left">
    <h2>Contribuer !</h2>

    <p>
      Vous pensez qu'il manque une question ? Envoyez-nous votre idée en remplissant le petit formulaire ci-dessous 👇
    </p>
    <p>
      Rappel des <span class="text-secondary">catégories</span>: <span v-for="category in categories" :key="category">{{ category }}, </span>...
    </p>

    <br />
    <hr class="custom-seperator" />
    <br />

    <form @submit.prevent="submitContribution" v-if="!contributionSubmitted">
      <h3 class="margin-bottom-0">
        <label for="question_text">Votre question <span class="color-red">*</span></label>
      </h3>
      <div class="help">
        <small><i>En 1 ou 2 phrases au maximum</i></small>
      </div>
      <input type="text" id="question_text" class="form-control" cols="95" v-model="contribution.question_text" placeholder="Que signifie le sigle GIEC ?" required />
      <h3 class="margin-bottom-0">
        <label for="text">Informations supplémentaires <small>(optionnel)</small></label>
      </h3>
      <div class="help">
        <small><i>La réponse et un peu d'explication, un lien pour aller plus loin, ...</i></small>
      </div>
      <textarea id="additional_info" class="form-control" rows="5" cols="95" v-model="contribution.additional_info" placeholder="C'est le Groupe d'experts Intergouvernemental sur l'Evolution du Climat. Plus d'infos ici: https://www.ecologique-solidaire.gouv.fr/comprendre-giec"></textarea>
      <p>
        <button type="submit" class="btn btn-outline-primary" :disabled="!contribution.question_text">📩&nbsp;Envoyer !</button>
      </p>
    </form>

    <div v-if="contributionSubmitted && loading" class="loading">
      Envoi de votre contribution...
    </div>

    <div v-if="contributionSubmitted && error" class="error">
      <h3>Il y a eu une erreur 😢</h3>
      {{ error }}
    </div>

    <div v-if="contributionSubmitted && contributionResponse">
      <h3>Merci beaucoup 💯</h3>
      <p>On fera de notre mieux pour prendre en compte votre contribution.</p>
    </div>

    <br />
    <br />
    <div class="row text-center justify-content-end">
      <div class="col-sm">
        <div v-if="contributionSubmitted" @click="init()">
          ✍️&nbsp;Nouvelle contribution
        </div>
      </div>
      <div class="col-sm">
        <router-link :to="{ name: 'about' }">
          ℹ️&nbsp;À propos de cette application
        </router-link>
      </div>
      <div class="col-sm">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import HomeLink from './HomeLink.vue'

export default {
  name: 'Contribute',
  components: {
    HomeLink
  },

  data() {
    return {
      categories: ['action', 'biodiversité', 'climat', 'consommation', 'énergie', 'histoire', 'pollution', 'ressources', 'science', 'autre'],
      contribution: {
        question_text: "",
        additional_info: ""
      },
      contributionSubmitted: false,
      contributionResponse: null,
      loading: false,
      error: null,
    }
  },

  mounted () {
    this.init();
  },

  methods: {
    init() {
      this.contribution = {
        question_text: "",
        additional_info: ""
      },
      this.contributionSubmitted = false;
      this.contributionResponse = null;
      this.loading = false;
      this.error = null;
    },
    submitContribution() {
      this.contributionSubmitted = true;
      this.error = this.contributionResponse = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/contribute`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.contribution)
      })
        .then(response => {
          this.loading = false
          return response.json()
        })
        .then(data => {
          this.contributionResponse = data;
        })
        .catch(error => {
          console.log(error)
          this.error = error;
        })
    }
  }
}
</script>

<style scoped>
</style>
