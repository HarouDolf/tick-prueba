<template>
    <div class="hello">
        <div>
          <br>
            <h1 class="text-center">Registro de solicitudes</h1>
            <br>
            <div id="first" class="row justify-content-center">
              <div class="col-auto">
  
                <table table class="table table-striped">
                    <tr>
                        <th scope="col">Nombre Solicitante</th>
                        <th scope="col">Nombre Seguidor</th>
                    </tr>
                    <tbody>
                        <tr v-for="(data, index) in data" :key="index">
                            <td class="td1">{{ data.Requester }}</td>
                            <td class="td2">{{ data.Follower }}</td>
                        </tr>
                    </tbody>
                </table>
                </div>
            </div>
        </div>
      </div>
  </template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import { internet } from '@/utils/Internet';
	import { AxiosResponse } from 'axios';
	import Util from '@/utils/Util';
	@Component({
		name: 'AgentView',
	})
        
	export default class AgentView extends Vue {
    public isLoading = false;
	data () {
        return {
            data: []
        }
    }

	mounted(): void {
		this.getData();
	}

	private getData(): void {
			this.isLoading = true;
			const request_PruebaConexion = internet
				.newRequest()
				.get(
					`modelgetall`
				);
			Util.waitForPromises([
				request_PruebaConexion,
			])
				.then((responses) => {
					const response_1 = responses[0] as AxiosResponse;
                    let ticket = this.data
                    this.data= ticket+response_1.data
                    console.log(this.data)
				})
				.catch(console.log)
				.finally(() => {
					this.isLoading = false;
				});
		}
	}
</script>