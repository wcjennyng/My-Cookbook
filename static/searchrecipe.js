//Search a Recipe 

async function searchForm(e) {
    e.preventDefault()
    try {
        const res = await axios({
            method: 'post',
            url: '/api/searchrecipe',
            data: {
                name: $('#name').val()
            }
        })

        handleResponse(res);
        $('#name-form').trigger('reset')


    } catch (error) {
        const err = error.response.data
        for (key in err) {
            $('#name_err').html(err[key])
        }

    }
}


function handleResponse(res) {
    $('#name_err').html('')
    $('#search-results').empty()
    const searchRecipes = res.data.meals_arr
    console.log('res data', res.data)
    console.log('searchRecipes', searchRecipes)
    if (searchRecipes == null || searchRecipes == undefined) {
        $('#name_err').html('Recipe not found. Please choose another recipe name.')
    } else {
        for (let r = 0; r < searchRecipes.length; r++) {
            const recipe = searchRecipes[r];
            console.log(recipe)
            $(document).ready(function () {
                $('#add-fav-' + r).click(async function () {
                    console.log('addfav', r)
                    let msg = 'Added to Favorites!'
                    $(`#success-msg-${r}`).append(document.createTextNode(msg)).css('color', 'green')
                    const res = await axios({
                        method: 'post',
                        url: `/users/${username}/favorites`,
                        data: { fav: recipe }

                    })


                })

            })


            $('#search-results').append(`
            
            <div id='accordion'>
                <div class="card mb-3 border-info" style='max-width: 20rem; min-width: 20rem;'>
            
                    <img class='img-thumbnail' width='320' height='320' style="text-align: center; " src='${recipe.strMealThumb}'
                    alt="Card image cap">
              
                        <div class="card-body">
                            <input type="hidden" name="meal_id" value="${recipe.idMeal}">
                            <h4 class="card-title text-dark">${recipe.strMeal}</h4>
                            <hr>
                            <h5>
                                <button class="btn mb-1" data-toggle="collapse" data-target="#collapseInstructions-${r}" aria-expanded="true" aria-controls="collapseInstructions-${r}">
                                    Instructions
                                </button>
                            </h5>
                            <div id="collapseInstructions-${r}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                            <div class="card-body">
                                <p class="card-text">${recipe.strInstructions}</p>
                            </div>
                            </div>
                
                            <h5>
                                <button class="btn mb-2" data-toggle="collapse" data-target="#collapseIng-${r}" aria-expanded="true" aria-controls="collapseIng-${r}">
                                    Ingredients
                                </button>
                            </h5>
                            <div id="collapseIng-${r}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
                            <div class="card-body">
                                <ul id="ingredients${r}"></ul>
                            </div>
                            </div> 
                
                            
                            <button id="add-fav-${r}" class="btn mb-1"><i class="material-icons" style='color: lightpink; vertical-align: bottom;'>favorite</i> </button>
                            <div id='success-msg-${r}'></div>
                        </div>
                
                </div>    
            </div>            
                `)
            for (let i = 1; i < 20; i++) {
                const measure = recipe['strMeasure' + i]
                const ingredient = recipe['strIngredient' + i]
                if (ingredient && measure) {
                    $('#ingredients' + r).append(`<li>${measure} ${ingredient}</li>`)
                }
            }
        }


    }



}

$('#name-form').on('submit', searchForm)

$(function () {
    $('.collapse').collapse()
})


