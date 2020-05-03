<template>
  <section class="text-align-left">
    <h2>Contribuer !</h2>

    <p>
      Vous souhaitez rajouter une question ? Ou faire un commentaire sur le contenu existant ?<br />
      Envoyez-nous ça en remplissant le petit formulaire ci-dessous 👇
    </p>

    <br />
    <hr class="custom-seperator" />
    <br />

    <form @submit.prevent="submitContribution" v-if="!contributionSubmitted">
      <div class="form-group">
        <h3 class="margin-bottom-0">
          <label for="contribution_type">Ma contribution est ...</label>
        </h3>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline1" name="customRadioInline1" class="custom-control-input" value="nouvelle question" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline1">Une nouvelle question</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline2" name="customRadioInline1" class="custom-control-input" value="commentaire application" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline2">Un commentaire sur l'application</label>
        </div>
      </div>
      
      <div class="form-group" v-if="contribution.type === 'nouvelle question'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre question <span class="color-red">*</span></label>
        </h3>
        <div class="help">
          <small><i>En 1 ou 2 phrases au maximum</i></small>
        </div>
        <input type="text" id="contribution_text" class="form-control" v-model="contribution.text" placeholder="Que signifie le sigle GIEC ?" required />
      </div>
      <div class="form-group" v-if="contribution.type === 'nouvelle question'">
        <h3 class="margin-bottom-0">
          <label for="text">Informations supplémentaires <small>(optionnel)</small></label>
        </h3>
        <div class="help">
          <small><i>La réponse et un peu d'explication, un lien pour aller plus loin, ...</i></small>
        </div>
        <textarea id="description" class="form-control" rows="5" v-model="contribution.description" placeholder="C'est le Groupe d'experts Intergouvernemental sur l'Evolution du Climat. Plus d'infos ici: https://www.ecologique-solidaire.gouv.fr/comprendre-giec"></textarea>
      </div>

      <div class="form-group" v-if="contribution.type !== 'nouvelle question'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre commentaire <span class="color-red">*</span></label>
        </h3>
        <div class="help">
          <small><i>Lâchez-vous :)</i></small>
        </div>
        <textarea id="contribution_text" class="form-control" rows="5" v-model="contribution.text" required></textarea>
      </div>
      
      <div class="form-group">
        <p>
          <button type="submit" class="btn" :class="contribution.text ? 'btn-primary' : 'btn-outline-primary'" :disabled="!contribution.text">📩&nbsp;Envoyer !</button>
        </p>
      </div>
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
    <hr />
    <div class="row actions text-center justify-content-end">
      <div class="col-sm">
        <div v-if="contributionSubmitted" @click="init()">
          <a href="#">✍️&nbsp;Nouvelle contribution</a>
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
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'Contribute',
  components: {
    HomeLink
  },

  data() {
    return {
      contribution: {
        text: "",
        description: "",
        type: "nouvelle question"
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
        text: "",
        description: "",
        type: "nouvelle question"
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
