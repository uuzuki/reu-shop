// Инициализация платежа
async function initPayment(amount, description, orderId) {
    const response = await fetch('https://api.yookassa.ru/v3/payments', {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa('shopId:shopSecretKey'),
        'Content-Type': 'application/json',
        'Idempotence-Key': orderId
      },
      body: JSON.stringify({
        amount: {
          value: amount,
          currency: "RUB"
        },
        capture: true,
        confirmation: {
          type: "redirect",
          return_url: "https://вашсайт.ru/order/success"
        },
        description: description
      })
    });
    return await response.json();
  }
  
  // Обработка кнопки оплаты
  document.getElementById('pay-btn').addEventListener('click', async () => {
    const payment = await initPayment(5000, "Заказ №12345", "order-12345");
    window.location.href = payment.confirmation.confirmation_url;
  });