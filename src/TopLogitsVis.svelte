<script>
    import { sparse_color_map_neuron_css } from "./shared_utils/colors";

    export let pos_logit_tokens
    export let neg_logit_tokens
    export let pos_logit_values
    export let neg_logit_values
    export let default_display
    export let max_display
    export let name

    var num_logits = default_display

    // OK what's up? 
    // I pass in a 1D vector of activations, and need to plot a list of tokens, each coloured by the activation of the corresponding token

    // var activations_array = [];
    // for (var i = 0; i < activations.shape[0]; i++) {
    //     activations_array.push(activations.data[i]);
    // }
    // console.log(activations_array)
    // console.log(activations)

    // var max_activation = Math.max(...activations_array);
    // var min_activation = Math.min(...activations_array);
    // var scaled_activations = activations_array.map(x => x / Math.max(max_activation, Math.abs(min_activation)));
    // console.log(max_activation)
    // console.log(scaled_activations)
    
    // var all_token_colors = scaled_activations.map((x) => sparse_color_map_neuron_css(x));
</script>
<div class="input-element">
    <select class="input-element__select" bind:value={num_logits}>
        {#each [1, 2, 5, 10, 20, 50] as i}
            {#if i <= max_display}
                <option value={i}>{i}</option>
            {/if}
        {/each}
    </select>
</div>

<div>Displaying {num_logits} logits!</div>


<!-- <div class="tokens-container">
    <div class="figcaption" style="grid-column: left;">
        {#if neuron_name!=""}Name: {neuron_name}. {/if}Max act: {max_activation.toFixed(5)}. Min act: {min_activation.toFixed(5)}
    </div>
    <div class="tokens">
        {#each tokens as tok, tok_i}
            
              <span
                    class="token"
                    style="background: {all_token_colors[tok_i]};">{tok}</span>
        {/each}
    </div>
</div> -->


<style>
    .tokens-container {
        display: grid;
        grid-template-rows: [title] min-content [main] min-content;
        grid-template-columns: [left] min-content [right] minmax(min-content, 800px) [end];
        gap: 12px;
        margin-top: 24px;
    }
    .tokens {
        grid-row: main;
        grid-column-start: left;
        grid-column-end: end;
        cursor: pointer;
        height: min-content;
        line-height: 125%;
        font-size: 14px;
    }
    .tokens .token {
        white-space: pre-wrap;
        border: 1px solid rgb(203, 203, 203);
        z-index: 10;
    }
    .figcaption {
        color: #888;
        grid-row: title;
        white-space: nowrap;
        font-weight: 700;
    }
    
</style>
