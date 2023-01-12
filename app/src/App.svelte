<script lang="ts">
  import { onMount } from "svelte";

  let model = "ada";
  const pricing = {
    ada: 0.0004,
    babbage: 0.0005,
    curie: 0.002,
    davinci: 0.02,
  };

  interface Metadata {
    emb: {
      [key: string]: {
        absdate: number;
        fmtdate: string;
        token_size: number;
      };
    };
    regen: string[];
    src: {
      [key: string]: {
        absdate: number;
        fmtdate: string;
        token_size: number;
      };
    };
  }

  let search = "";
  let search_result: any;
  let selected_file: string;

  let file_metadata: Metadata | undefined;

  const process = async (e: any, filename: string) => {
    e.currentTarget.innerHTML = "Loading...";
    e.currentTarget.disabled = true;
    const res = await fetch(`http://localhost:5000/process?f=${filename}`);
    file_metadata = await res.json();
  };

  const embed = async (e: any, filename: string, model: string) => {
    e.currentTarget.innerHTML = "Loading...";
    e.currentTarget.disabled = true;
    const res = await fetch(
      `http://localhost:5000/embed?f=${filename}&model=${model}`
    );
    file_metadata = await res.json();
  };

  const query = async (e, q, f, model) => {
    e.currentTarget.innerHTML = "Loading...";
    e.currentTarget.disabled = true;
    const res = await fetch(
      `http://localhost:5000/search?f=${f}&model=${model}&q=${q}`
    );
    search_result = await res.json();
    e.currentTarget.disabled = false;
    e.currentTarget.innerHTML = "Search";
  };

  onMount(async () => {
    const res = await fetch("http://localhost:5000/metadata");
    file_metadata = await res.json();
    console.log(file_metadata);
  });
</script>

<main>
  <select class="px-3 py-2 rounded-xl" bind:value={model}>
    <option value="ada">Ada</option>
    <option value="babbage">Babbage</option>
    <option value="curie">Curie</option>
    <option value="davinci">Davinci</option>
  </select>
  <p>Source File:</p>
  <ul>
    {#if file_metadata}
      {#each Object.entries(file_metadata.src) as [file, data]}
        <li
          class={!file_metadata.regen.includes(file)
            ? "text-green-300"
            : "text-red-300"}
        >
          {file}
          {#if !data?.token_size}
            <span class="font-bold"> (Not yet processed) </span>
          {/if}
          <span class="opacity-75">({data.fmtdate})</span>
        </li>
      {/each}
    {:else}
      <p>Loading...</p>
    {/if}
  </ul>

  <p>Embedded:</p>
  <ul>
    {#if file_metadata}
      {#if Object.keys(file_metadata?.emb).length !== 0}
        {#each Object.entries(file_metadata.emb) as [file, data]}
          <li>
            {file}: {data.fmtdate}
          </li>
        {/each}
      {:else}
        <div>The source data hasn't been embedded yet</div>
      {/if}
    {:else}
      <p>Loading...</p>
    {/if}
  </ul>

  <p>Needs Processing:</p>
  <ul>
    {#if file_metadata}
      {#each file_metadata.regen as file}
        <li
          class="{file_metadata.src[file].token_size
            ? 'text-green-300'
            : 'text-red-300'} mb-4"
        >
          {file}
          {#if file_metadata.src[file].token_size}
            ({`${file_metadata.src[file].token_size} Token`})
            <button
              on:click={(e) => embed(e, file, model)}
              class="px-2 text-white transition-colors bg-green-700 rounded-md hover:bg-green-900"
              >Embed ({`$${
                Math.round(
                  (file_metadata.src[file].token_size / 1000) *
                    pricing[model] *
                    10000
                ) / 10000
              }`})</button
            >
          {:else}
            (Unprocessed)
            <button
              on:click={async (e) => await process(e, file)}
              class="px-2 text-white transition-colors bg-red-700 rounded-md hover:bg-red-900"
              >Process</button
            >
          {/if}
        </li>
      {/each}
    {:else}
      <p>Loading...</p>
    {/if}
  </ul>

  <p class="mt-10 text-center">Search</p>
  {#if file_metadata}
    <select bind:value={selected_file} class="px-3 py-2 rounded-lg">
      {#if Object.keys(file_metadata?.emb).length !== 0}
        {#each Object.entries(file_metadata.emb) as [file, data]}
          <option value={file}>
            {file}
          </option>
        {/each}
      {/if}
    </select>
  {:else}
    <p>Loading...</p>
  {/if}
  <input
    placeholder="type your search query here..."
    class="px-3 py-1 rounded-lg"
    type="text"
    bind:value={search}
  />
  <button
    on:click={async (e) => await query(e, search, selected_file, model)}
    class="px-3 py-2 text-white bg-gray-800 rounded-lg">Search</button
  >
  {#if search_result}
    {#each search_result["text"] as txt, i}
      <li>
        <p>{txt}</p>
        <p>({search_result["similiarities"][i]})</p>
      </li>
    {/each}
  {/if}
</main>

<style>
</style>
