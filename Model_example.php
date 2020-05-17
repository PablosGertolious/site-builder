<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Support\Facades\DB;

/**
 * @property string id The ID of this collective.
 */
class Country extends Model
{
    use SoftDeletes;

    protected $dates = ['deleted_at'];
    protected $fillable = ['name','slug','abbreviation','code','is_active'];

    // By default, we won't show these in the JSON representation.
    protected $hidden = ['created_at', 'updated_at', 'deleted_at'];
    protected $guarded = array();


    public static function boot()
    {
        parent::boot();

        static::creating(function ($model) {

            $tempSlug = $model->name;

            $model->slug = str_slug($tempSlug);// change the ToBeSluggiefied

            $baseSlug =
                static::whereRaw("slug = '$model->slug'")
                    ->latest('id')
                    ->value('slug');

            if ($baseSlug) {
              $latestSlug =
                  static::whereRaw("(slug = '$model->slug' or slug LIKE '$model->slug-%')")
                      ->latest('id')
                      ->value('slug');
                if ($latestSlug) {
                    $pieces = explode('-', $latestSlug);

                    $number = intval(end($pieces));

                    $model->slug .= '-' . ($number + 1);
                } else {
                    $model->slug .= '-1';
                }
            }
        });

        static::updating(function ($model) {

            // Only do the slug check if changing
            $newSlug = str_slug($model->name);
            if ($model->slug != $newSlug) {
                $model->slug = $newSlug;

                $baseSlug =
                  static::whereRaw("id!=$model->id AND slug = '$model->slug'")
                      ->latest('id')
                      ->value('slug');

                if ($baseSlug) {
                  $latestSlug =
                    static::whereRaw("id!=$model->id AND slug LIKE '$model->slug-%'")
                        ->latest('id')
                        ->value('slug');
                    if ($latestSlug) {
                        $pieces = explode('-', $latestSlug);

                        $number = intval(end($pieces));

                        $model->slug .= '-' . ($number + 1);
                    } else {
                        $model->slug .= '-1';
                    }
                }
            }
        });

    }

}
