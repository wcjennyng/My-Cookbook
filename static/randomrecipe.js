// Random Recipe when searching with a letter

async function RandomForm(e) {
    e.preventDefault()
    try {

        const resp = await axios({
            method: 'post',
            url: '/api/randomrecipe',
            data: {
                letter: $('#letter').val()
            }
        })



        handleResponse(resp);
        $('#random-form').trigger('reset')



    } catch (error) {
        const err = error.response.data
        for (key in err) {
            $('#random_err').html(err[key])
        }

    }
}

function handleResponse(res) {
    $('#random_err').html('')
    $('#random-results').empty()
    $('#ranbtn-results').empty()
    const randomRecipe = res.data.recipe_arr
    if (randomRecipe == null || randomRecipe == undefined) {
        $('#random_err').html('Recipe not found. Please choose another letter.')
    } else {
        const r = Math.floor(Math.random() * randomRecipe.length)
        const recipe = randomRecipe[r]
        $('#random-results').append(`
                        <div class="col-sm-12 col-md-6 col-lg-6 d-flex flex-row justify-content-center m-auto">
                            <div class="card mb-3 border-info">
                                <h4 class="card-header bg-transparent text-dark mb-3">${recipe.strMeal}</h4>
                                <img class="justify-content-center m-auto" src="${recipe.strMealThumb}" width="200" height="200">
                                <h5 class="mt-2"><b>Instructions:</b></h5>
                                <p class="card-text mx-2">${recipe.strInstructions}</p>
                                <h5><b>Ingredients:</b></h5>
                                <ul style="list-style:none; padding-left:0;" id="ingredients"></ul>
                            </div>
                        </div>`)
        for (let i = 1; i < 20; i++) {
            const measure = recipe['strMeasure' + i]
            const ingredient = recipe['strIngredient' + i]
            if (ingredient && measure) {
                $('#ingredients').append(`<li>${measure} ${ingredient}</li>`)
            }
        }


    }

}



$('#random-form').on('submit', RandomForm)

//RANDOM BUTTON

$('#random-btn').on('submit', async function (e) {
    e.preventDefault();
    const res = await axios.get("https://www.themealdb.com/api/json/v1/1/random.php")
    moreRandom(res.data)
})

function moreRandom(resp) {
    $('#random_err').html('')
    $('#random-results').empty()
    $('#ranbtn-results').html('')
    const arr = resp['meals'][0]
    $('#ranbtn-results').append(`<div class="col-sm-12 col-md-6 col-lg-6 d-flex flex-row justify-content-center m-auto">
                                <div class="card mb-3 border-info">
                                <h4 class="card-header bg-transparent text-dark mb-3">${arr.strMeal}</h4>
                                <img class="justify-content-center m-auto" src="${arr.strMealThumb}" width="200" height="200">
                                <h5 class="mt-2"><b>Instructions:</b></h5>
                                <p class="card-text mx-2">${arr.strInstructions}</p>
                                <h5><b>Ingredients:</b></h5>
                                <ul id="ingredients"></ul>
                                </div>
                                </div>`)
    for (let i = 1; i < 20; i++) {
        const measure = arr['strMeasure' + i]
        const ingredient = arr['strIngredient' + i]
        if (ingredient && measure) {
            $('#ingredients').append(`<li>${measure} ${ingredient}</li>`)
        }
    }
}



