<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Models\Item;

class ItemController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * 商品一覧
     */
    public function index()
    {
        // 商品一覧取得
        $items = Item::all();

        return view('item.index', compact('items'));
    }

    /**
     * 商品登録
     */
    public function add(Request $request)
    {
        // POSTリクエストのとき
        if ($request->isMethod('post')) {
            // バリデーション
            $this->validate($request, [
                'name' => 'required|max:20',
                'image' => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
                'detail' => 'required|max:100',
            ],[
                'name.required' => '車名は必須です',
                'name.max' => '車名は20文字までです',
                'image.required' => '画像は必須です',
                'image.max' => '画像サイズが大きすぎて添付できません',
                'detail.required' => '詳細は必須です',
                'detail.max' => '詳細は100文字以下です'
            ]);

            $image = null;
            if($request->image){
                $image = base64_encode(file_get_contents($request->image->getRealPath()));
            }
            

            // 商品登録
            Item::create([
                'user_id' => Auth::user()->id,
                'name' => $request->name,
                'image' => $image,
                'detail' => $request->detail,
            ]);

            return redirect('/items');
        }

        return view('item.add');
    }

    /**
     * 商品編集画面表示
     */
    public function edit($id){
        $item = Item::find($id);
        return view('item.edit', ['item'=>$item]);
    }

    /**
     * 商品更新
     */
    public function update(Request $request){
        // バリデーション
        $this->validate($request, [
            'name' => 'required|max:20',
            'image' => 'required',
            'detail' => 'required|max:100',
        ],[
            'name.required' => '車名は必須です',
            'name.max' => '車名は20文字までです',
            'image.required' => '画像は必須です',
            'detail.required' => '詳細は必須です',
            'detail.max' => '詳細は100文字以下です'
        ]);
        $item = Item::find($request->id);
        $item->name = $request->name;
        $item->detail = $request->detail;
        if($request->image){
            $image = base64_encode(file_get_contents($request->image->getRealPath()));
            $item->image = $image;
        }
        $item->save();
        return redirect('/items');
    }

    /**
     * 商品削除
     */
    public function delete(Request $request)
    {
        $item = Item::find($request->id);
        $item->delete();
        
        return redirect('/items');
    }
}
