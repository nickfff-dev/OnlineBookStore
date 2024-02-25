#!/usr/bin/python3
""" module for the checkout blueprint """
from models import storage
from models.order import Order
from models.order_line import OrderLine
from models.book import Book
from models.user import User
from models.order_status import OrderStatus
from web_dynamic.blue_prints import bookstore_views
from datetime import datetime
from flask import jsonify, request, g, make_response, session, render_template, redirect, url_for

# sample session['orderlines]
# {'b9bc3e41-ced1-416d-a556-9c6259bae75e': {'edition': 'Atria books export ed.', 'image': 'https://prestigebookshop.com/wp-content/uploads/2019/02/book-image-5309.jpg', 'isbn': '9781416549178', 'quantity': 1, 'sub-total': 750.0, 'title': "My sister's keeper", 'unitSalePrice': 750.0}, 'd8d19a70-0d32-4897-a320-6e52dd5f430a': {'edition': 'printing (13)', 'image': 'https://kibangabooks.com/wp-content/uploads/2023/11/The-HANDMAIDS-TALE-book-by-Author-Margaret-Atwood1680418916.jpeg', 'isbn': '9781784873189', 'quantity': 1, 'sub-total': 1250.0, 'title': "The Handmaid's Tale", 'unitSalePrice': 1250.0}, 'fb6f6053-a4cc-4d3e-b887-f61819a8ed38': {'edition': 'First edition.', 'image': 'https://prestigebookshop.com/wp-content/uploads/2019/02/book-image-17964.jpg', 'isbn': '9780316267397', 'quantity': 1, 'sub-total': 2890.0, 'title': 'Kennedy and King', 'unitSalePrice': 2890.0}}
@bookstore_views.route('/checkout', methods=['GET', 'POST'], strict_slashes=False)
def checkout():
    """ checkout route """
    if request.method == 'GET':
        order_lines =  session.get('orderlines', {})
        if len(order_lines) == 0:
            return redirect(url_for('bookstore_views.index'))
        user = storage.get(User, session['user_id'])
        if user is None:
            return redirect(url_for('bookstore_views.index'))
        total = 0
        cart_items = []
        for key, value in order_lines.items():
            total += value['sub-total']
            item = {
                'book_id': key,
                'order_id': '',
                'quantity': value['quantity'],
                'sub_total': value['sub-total'],
                'unit_sale_price': value['unitSalePrice']
            }
            cart_items.append(item)
        order_data ={
            'user_id': session['user_id'],
            'order_date': datetime.utcnow(),
            'total': total
        }
        order = Order(**order_data)
        order.save()
        for item in cart_items:
            item['order_id'] = order.id
            order_line = OrderLine(**item)
            order_line.save()
            order.orderlines.append(order_line)
            book = storage.get(Book, item['book_id'])
            book.unitsInStock -= item['quantity']
            book.orderlines.append(order_line)
            item = order_line.to_dict()
            item.update({'title': book.title, 'image': book.image, 'edition': book.edition})
        order_status = OrderStatus(status='Pending', order_id=order.id, is_current=True)
        order_status.save()
        order.statuses.append(order_status)
        storage.save()
        session.pop('orderlines')
        session.modified = True
        return render_template('checkout.html', order=order.to_dict(), order_lines=cart_items)