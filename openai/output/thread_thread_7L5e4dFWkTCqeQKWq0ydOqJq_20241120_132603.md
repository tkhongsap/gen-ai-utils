# Conversation Thread

[35mTime: 2024-11-18 10:41:38
Role: user
Content: apiVersion: apps/v1
kind: Deployment
metadata:
  name: otc-nsi-bff-mobile-deployment
  labels:
    app: otc-nsi-bff-mobile-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: otc-nsi-bff-mobile
  template:
    metadata:
      labels:
        app: otc-nsi-bff-mobile
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - otc-nsi-bff-mobile
                topologyKey: kubernetes.io/hostname
      containers:
        - name: otc-nsi-bff-mobile
          image: registryii.thaibevapp.com/otcsell/newsalesintelligence/bff-mobile:0.0.1
          imagePullPolicy: Always
          ports:
            - containerPort: 80
          env:
            - name: ASPNETCORE_ENVIRONMENT
              value: Development
            - name: PORT
              value: "80"
          envFrom:
            - secretRef:
                name: otc-nsi-secret-elk
          resources:
            requests:
              memory: "300Mi"
              cpu: "200m"
            limits:
              memory: "600Mi"
              cpu: "400m"
[0m
==================================================
[34mTime: 2024-11-18 10:41:42
Role: assistant
Content: Here's a review of the provided Kubernetes deployment YAML for `otc-nsi-bff-mobile-deployment` across the key dimensions:

### Code Review Summary

**Correctness and Functionality**
- **Score: 9/10**
- **Explanation:** The deployment configuration appears correctly defined, with appropriate fields for the deployment spec and pod template. The `replicas`, `selector`, and `template` match labels are set correctly. However, without running this in an actual Kubernetes environment, some minor functional issues could remain undetected.
- **Improvement Suggestion:** Make sure that the referenced secret, `otc-nsi-secret-elk`, exists in the target namespace before deployment.

**Code Quality and Maintainability**
- **Score: 8/10**
- **Explanation:** The YAML is organized and easy to read. Proper indentation and structural organization are maintained. Using explicit labels and selectors improves clarity. However, the environment variable `ASPNETCORE_ENVIRONMENT` is hardcoded as Development which might not be ideal for all contexts (e.g., production).
- **Improvement Suggestion:** Consider using different configurations or secrets for different environments (e.g., Production, Staging) to make it more flexible.

**Performance and Efficiency**
- **Score: 8/10**
- **Explanation:** Resource requests and limits are defined, which allows the Kubernetes scheduler to make informed decisions. This is good for performance management. However, the deployment uses a single replica, which could be a performance bottleneck if traffic increases.
- **Improvement Suggestion:** If this application requires high availability or load balancing, consider increasing the `replicas` count.

**Security and Vulnerability Assessment**
- **Score: 7/10**
- **Explanation:** The usage of environment variables to pass configurations is a good practice, but environment variables can expose sensitive information if not handled properly. It is important to ensure that the secret and its contents are secured properly. Also, it would be helpful to define a security context.
- **Improvement Suggestion:** Define a security context to limit user privileges and run the pod with a non-root user if applicable.

**Code Consistency and Style**
- **Score: 9/10**
- **Explanation:** The YAML adheres to Kubernetes conventions. Naming is consistent and aligns across the metadata and spec sections, which enhances readability and maintainability.
- **Improvement Suggestion:** Ensure consistent use of naming throughout the entire project for better coherence.

**Scalability and Extensibility**
- **Score: 7/10**
- **Explanation:** The current setup is functional, but the single replica limits scalability. The deployment would require updates in the YAML to enable horizontal scaling or readiness probes to manage the state of the application better.
- **Improvement Suggestion:** Implement a readiness probe to ensure the application is fully up and functional before routing traffic and consider configurations to support auto-scaling.

**Error Handling and Robustness**
- **Score: 8/10**
- **Explanation:** The configuration does not explicitly define any error-handling specifications like liveness and readiness probes; however, there is a basic setup facilitating standard functionality. Error handling depends largely on the application itself.
- **Improvement Suggestion:** Add liveness and readiness probes to enhance the robustness of the deployment.

### Overall Score: 7.86/10

### Code Improvement Summary:
1. **Environment Flexibility:** Consider externalizing the `ASPNETCORE_ENVIRONMENT` variable to allow different environments.
2. **Increase Replicas:** If applicable, increase the `replicas` value to ensure better availability and load handling.
3. **Security Context:** Define a security context for the deployment to mitigate security vulnerabilities, such as running in non-root context.
4. **Readiness and Liveness Probes:** Implement readiness and liveness probes for better resilience in production use.
5. **Namespace Awareness:** Ensure that referenced resources, like the secret, are available in the Kubernetes namespace where the deploy is intended to run.

This review should provide insights into the current state and potential improvements for this Kubernetes deployment configuration.[0m
==================================================
[35mTime: 2024-11-18 10:43:10
Role: user
Content: import {CommonModule} from '@angular/common';
import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {NgbModal, NgbModalRef} from '@ng-bootstrap/ng-bootstrap';
import {selectOption} from '../../../goods-reservation/models/responses/product-response.model';
import {DropdownlistComponent} from '../../../shared/components/dropdown-list/dropdown-list.component';
import {StorageService} from '../../../shared/services/storage.service';
import {InfoModalComponent} from '../../../shared/components/modals/info-modal/info-modal.component';
import {SaleOrderProduct} from '../../models/response/sales-order.model';
import {SalesOrderService} from '../../services/sales-order.service';
import {Product, Transaction} from '../../../shared/models/take-order-product.model';
import {TakeOrderDetailComponent} from '../take-order-detail/take-order-detail.component';
import {Subscription, firstValueFrom} from 'rxjs';
import {Promotions} from '../../../shared/models/promotion-detail.model';
import {
    PromotionDetailModalComponent
} from '../../../shared/components/promotion-detail-modal/promotion-detail-modal.component';
import {ModalStateService} from '../../../shared/services/modal-state.service';
import {State} from '../../../shared/enums/event-action.enum';
import {VehicleStocksService} from '../../../shared/services/vehicle-stocks.service';
import {RouteService} from '../../../shared/services/route.service';
import {ActivatedRoute} from '@angular/router';
import {QueryParamsKey} from '../../../shared/models/storage.model';

@Component({
    selector: 'app-take-order-product',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        TakeOrderDetailComponent,
        DropdownlistComponent,
    ],
    templateUrl: './take-order-product.component.html',
    styleUrl: './take-order-product.component.scss',
})
export class TakeOrderProductComponent implements OnInit, OnDestroy {
    @Input() documentNo: string = '';
    @Input() productGroups: selectOption[] = [];

    @Output() totalPriceChange = new EventEmitter<number>();
    @Output() saleproductorder: EventEmitter<Product[]> = new EventEmitter<Product[]>();
    @Output() isChangeQty = new EventEmitter<boolean>();

    totalPrice: number = 0.0;
    takeOrderProduct: Product[] = [];
    selectedProducts: Product[] = [];
    searchText: string = '';
    titleName = 'รายการสินค้า';
    productGroupId: string = '0';
    companyCode: string = '';
    currentDate = new Date();
    saleDate: string = this.currentDate.toISOString().split('T')[0];

    product: Product = {salesQuantity: 0, baseQuantity: 0} as Product;
    salesOrder: SaleOrderProduct[] = [];

    salesReservationPrice: number = 0;
    baseReservationPrice: number = 0;

    modalRef!: NgbModalRef;

    salesTeamCode: string = '';

    subscription: Subscription = new Subscription();
    isModalOpen: boolean = false;

    constructor(
        private takeOrderProductService: VehicleStocksService,
        private salesOrderService: SalesOrderService,
        private storageService: StorageService,
        private modalService: NgbModal,
        private modalStateService: ModalStateService,
        private routeService: RouteService,
        private route: ActivatedRoute,
    ) {
    }

    ngOnDestroy(): void {
        this.subscription.unsubscribe();
    }

    //TODO: Move SaleOrder GoodsCarries Category to TakeOrderPage
    async ngOnInit(): Promise<void> {
        await this.setStorage();
        await this.setDocumentNo();
        this.subscription = this.modalStateService.isModalOpen$.subscribe(isOpen => {
            this.isModalOpen = isOpen;
        });

        this.companyCode = this.storageService.getCompanyCode();
        this.salesTeamCode = this.storageService.getSalesTeamCode();

        await this.loadInitialData();
    }

    async setStorage() {
        await this.routeService.setQueryParamsToLocalStorage(this.route);
    }

    async setDocumentNo() {
        this.documentNo = await this.routeService.getValueFromQueryParams(QueryParamsKey.DocumentNo, this.route);
    }

    async loadInitialData(): Promise<void> {
        this.takeOrderProduct = await this.getGoodsCarries();
        if (this.documentNo) {
            await this.getSalesOrder();
            this.renderProductWithSalesOrder();
        }
    }

    async getSalesOrder(): Promise<void> {
        const res = await firstValueFrom(this.salesOrderService.getSalesOrder(this.documentNo));
        this.salesOrder = res?.products || [];
    }

    onTotalPriceChange(newTotalPrice: number) {
        this.totalPriceChange.emit(newTotalPrice);
        this.onChangeQty(false);
    }

    setSelectedProductFromDocument() {
        if (!this.salesOrder.length) return;
        this.selectedProducts = this.salesOrder.map((product) => {
            const takeOrder = this.takeOrderProduct.find(
                (p) => p.code === product.code,
            );
            return {
                salesUnitName: product.saleUnit.name,
                salesQuantity: product.saleUnit.quantity,
                salesRate: product.saleUnit.salesRate,
                baseUnitName: product.baseUnit.name,
                baseQuantity: product.baseUnit.quantity,
                name: product.name,
                code: product.code,
                transactions: takeOrder?.transactions || [],
            } as Product;
        }) as Product[];
        this.saleproductorder.emit(this.selectedProducts);
    }

    async searchProduct(): Promise<void> {
        this.takeOrderProduct = [];
        const goodsCarries = await this.getGoodsCarries();
        this.takeOrderProduct = this.mapSelectedProductIntoTakeOrderProduct(goodsCarries);
        this.calculateTotalPrice();
    }

    mapSelectedProductIntoTakeOrderProduct(
        products: Product[],
    ): Product[] {
        return products.map(
            (product) => {
                const mapProduct = {...product, salesQuantity: 0, baseQuantity: 0} as Product;
                const productFound = this.selectedProducts.find(x => x.code == product.code);
                if (productFound) {
                    mapProduct.baseQuantity = productFound.baseQuantity;
                    mapProduct.salesQuantity = productFound.salesQuantity;
                }

                return mapProduct;
            },
        );
    }

    renderProductWithSalesOrder() {
        this.salesOrder.forEach((product) => {
            const index = this.takeOrderProduct.findIndex(
                (p) => p.code === product.code,
            );
            const isFound = index !== -1;

            if (isFound) {
                const saleUnitQTY = product.saleUnit.quantity;
                const baseUnitQTY = product.baseUnit.quantity;
                this.takeOrderProduct[index].baseQuantity = baseUnitQTY;
                this.takeOrderProduct[index].salesQuantity = saleUnitQTY;
                this.takeOrderProduct[index].baseReservedQuantity =
                    product.baseUnit.quantity;
                this.takeOrderProduct[index].salesRate =
                    product.saleUnit.salesRate;
            }
        });

        this.setSelectedProductFromDocument();
        this.calculateTotalPrice();
    }

    async getGoodsCarries(): Promise<Product[]> {
        const res = await firstValueFrom(this.takeOrderProductService
            .getGoodsCarries(
                this.saleDate,
                this.searchText,
                this.productGroupId,
                this.companyCode,
                this.salesTeamCode));

        return res.data ? res.data.products.map((x: Product) => ({...x, salesQuantity: 0, baseQuantity: 0})) : [];
    }

    productUpdated(inputProduct: Product): void {
        const product = inputProduct;
        const index = this.selectedProducts.findIndex(
            (x) => x.code == product.code,
        );
        const notFoundProduct = index == -1;
        if (notFoundProduct) {
            if (product.salesQuantity !== 0 || product.baseQuantity !== 0) {
                this.selectedProducts.push(product);
            }
        } else {
            if (this.isQuantityEmpty(product)) {
                this.selectedProducts.splice(index, 1);
            } else {
                this.selectedProducts[index].baseQuantity =
                    product.baseQuantity;
                this.selectedProducts[index].salesQuantity =
                    product.salesQuantity;
            }
        }

        this.calculateTotalPrice();
        this.saleproductorder.emit(this.selectedProducts);
        this.isChangeQty.emit(false);
    }

    isQuantityEmpty(product: Product): boolean {
        return !product.baseQuantity && !product.salesQuantity;
    }

    calculateTotalPrice(): void {
        this.totalPrice = 0;

        this.selectedProducts.forEach((p) => {
            const transactions = p.transactions;
            const totalSalePrice = p.salesQuantity * this.calculateTotalsSalesPrice(transactions);
            const totalBasePrice = p.baseQuantity * this.calculateTotalsBasePrice(transactions);
            this.totalPrice += totalSalePrice + totalBasePrice;
        });
        this.onTotalPriceChange(this.totalPrice);
    }

    async onSelectProductGroup(item: selectOption): Promise<void> {
        this.productGroupId = item.id;
        await this.searchProduct();
    }

    onChangeQty($event: boolean): void {
        this.isChangeQty.emit($event);
    }

    calculateTotalsSalesPrice(transactions: Transaction[]): number {
        this.salesReservationPrice = transactions.reduce((total, tx) => tx.saleReservationPrice, 0);
        return this.salesReservationPrice;
    }


    calculateTotalsBasePrice(transactions: Transaction[]): number {
        this.baseReservationPrice = transactions.reduce((total, tx) => tx.baseReservationPrice, 0);
        return this.baseReservationPrice;
    }

    openNotEnoughProduct() {
        this.modalStateService.openModal();
        const selectedQuantityMsg = this.inventoryWarningMessage();
        const remainingQuantityMsg = this.inventoryRemainingWarningMessage();
        const description = `<span class="fw-bold fs-5">${this.product.name}</span> <br> จำนวนสินค้าที่เลือก: ${selectedQuantityMsg}</br>  จำนวนสินค้าที่เหลือบนรถ: ${remainingQuantityMsg}</br>`;
        this.modalRef = this.modalService.open(InfoModalComponent, {centered: true, size: 'md'});
        this.modalRef.componentInstance.header = 'จำนวนสินค้าไม่เพียงพอ';
        this.modalRef.componentInstance.description = description;
        this.modalRef.componentInstance.acknowledgeLabel = 'รับทราบ';
        this.modalRef.closed.subscribe((res: boolean) => {
            if (res) {
                this.modalStateService.closeModal();
            }
        });

        this.modalRef.dismissed.subscribe(() => {
            this.modalStateService.closeModal();
        });
    }

    inventoryWarningMessage(): string {
        const saleRate = this.product.salesRate || 1;
        const totalBaseQuantity = this.product.baseQuantity;
        const totalSalesQuantity = this.product.salesQuantity;

        const saleUnit = Math.floor(totalBaseQuantity / saleRate) + totalSalesQuantity;
        const baseUnit = totalBaseQuantity % saleRate;

        const saleUnitMsg =
            saleUnit > 0 ? `<span class="fw-bold">${saleUnit}</span> ${this.product.salesUnitName}` : '';
        const baseUnitMsg =
            baseUnit > 0 ? `<span class="fw-bold">${baseUnit}</span> ${this.product.baseUnitName}` : '';

        return [saleUnitMsg, baseUnitMsg].filter(Boolean).join(', ');
    }

    inventoryRemainingWarningMessage(): string {
        const saleRate = this.product.salesRate || 1;
        const totalInvent = this.product.baseRemainingQuantity;

        const remainingSaleUnit = Math.floor(totalInvent / saleRate);
        const remainingBaseUnit = totalInvent % saleRate;

        const saleUnitMsg =
            remainingSaleUnit > 0 ? `<span class="fw-bold">${remainingSaleUnit}</span> ${this.product.salesUnitName}` : '';
        const baseUnitMsg =
            remainingBaseUnit > 0 ? `<span class="fw-bold">${remainingBaseUnit}</span> ${this.product.baseUnitName}` : '';

        return [saleUnitMsg, baseUnitMsg].filter(Boolean).join(', ');
    }

    convertToBaseTotalPrice(baseQuantity: number): number {
        return baseQuantity * this.baseReservationPrice;
    }

    convertToSaleTotalPrice(saleQuantity: number): number {
        return saleQuantity * this.salesReservationPrice;

    }

    convertToSaleQuantity(baseQuantity: number, product: Product): number {
        if (baseQuantity >= (product.salesRate || 0)) {
            return Math.floor(baseQuantity / (product.salesRate || 1));
        }
        return 0;
    }

    checkRoundUpSaleQuantity() {
        this.product.salesQuantity = this.verifyQuantity(this.product.salesQuantity);
        this.product.baseQuantity = this.verifyQuantity(this.product.baseQuantity);

        this.product.salesQuantity = Number(this.product.salesQuantity) + Number(this.convertToSaleQuantity(this.product.baseQuantity, this.product));
        this.product.baseQuantity = this.convertRemainingBaseQuantity(this.product.baseQuantity);

        this.productUpdated(this.product);
    }

    verifyQuantity(value: number | undefined | null): number {
        if ((value as number) < 0 || !value || value === Infinity) {
            return 0;
        }
        return value;
    }

    convertRemainingBaseQuantity(baseQuantity: number): number {
        return baseQuantity % (this.product.salesRate || 1);
    }

    updateQuantity(data: { action: string; product: Product; }, isBase: boolean): void {
        this.onChangeQty(false);
        this.product = data.product;
        const totalBaseRemaining = this.product.baseRemainingQuantity;

        if (data.action === State.Increase) {
            this.handleIncrease(isBase, totalBaseRemaining);
        } else if (data.action === State.Decrease) {
            this.handleDecrease(isBase);
        } else if (data.action === State.Adjust) {
            this.handleAdjust(totalBaseRemaining);
        }
        this.checkRoundUpSaleQuantity();
    }

    handleIncrease(isBase: boolean, totalBaseRemaining: number): void {
        if (isBase) {
            this.product.baseQuantity++;
        } else {
            this.product.salesQuantity++;
        }

        this.checkOverBaseRemaining(totalBaseRemaining);
    }

    handleDecrease(isBase: boolean): void {
        if (isBase && this.product.baseQuantity > 0) {
            this.product.baseQuantity--;
        } else if (!isBase && this.product.salesQuantity > 0) {
            this.product.salesQuantity--;
        }
    }

    handleAdjust(totalBaseRemaining: number): void {
        this.checkOverBaseRemaining(totalBaseRemaining);
    }

    checkOverBaseRemaining(totalBaseRemaining: number): void {
        const baseQuantity = Number(this.product.salesQuantity) * Number(this.product.salesRate) + Number(this.product.baseQuantity);
        if (baseQuantity > totalBaseRemaining) {
            this.openNotEnoughProduct();
            this.product.salesQuantity = Math.floor(totalBaseRemaining / this.product.salesRate);
            this.product.baseQuantity = totalBaseRemaining % Number(this.product.salesRate);
        }
    }

    openModalPromotion(promotions: Promotions[]): void {
        this.modalStateService.openModal();
        this.modalRef = this.modalService.open(PromotionDetailModalComponent, {centered: true, size: 'md'});
        this.modalRef.componentInstance.promotions = promotions;
        this.modalRef.closed.subscribe((res: boolean) => {
            if (res) {
                this.modalStateService.closeModal();
            }
        });

        this.modalRef.dismissed.subscribe(() => {
            this.modalStateService.closeModal();
        });

    }
}
[0m
==================================================
[34mTime: 2024-11-18 10:43:13
Role: assistant
Content: Here's a comprehensive review of the provided Angular component code for `TakeOrderProductComponent` across the key dimensions:

### Code Review Summary

**Correctness and Functionality**
- **Score: 8/10**
- **Explanation:** The component appears to implement its intended functionality correctly, including input handling, product selection, and total price calculations. However, potential issues could arise from asynchronous operations not handling exceptions properly, which may lead to unhandled promise rejections.
- **Improvement Suggestion:** Implement error handling for asynchronous calls to ensure any failed requests do not break the application flow. Consider adding `try-catch` blocks around async calls like `firstValueFrom`.

**Code Quality and Maintainability**
- **Score: 7/10**
- **Explanation:** The code is relatively well-structured, with a clear separation of concerns. The use of `async`/`await` enhances readability, but the code could benefit from further modularization. Some functions are quite long and handle multiple responsibilities, making them harder to read and maintain.
- **Improvement Suggestion:** Break down larger methods into smaller, more focused helper functions. For example, `loadInitialData`, `searchProduct`, and `getGoodsCarries` could be refactored to improve readability.

**Performance and Efficiency**
- **Score: 7/10**
- **Explanation:** The component makes multiple async calls, which could lead to performance bottlenecks, especially if some of these can be combined or optimized (e.g., fetching products and sales orders in parallel). Resource handling appears efficient overall, but there is room for improvement.
- **Improvement Suggestion:** Use `forkJoin` from RxJS to perform parallel requests where appropriate. This can significantly enhance performance, especially for the initial data loading.

**Security and Vulnerability Assessment**
- **Score: 6/10**
- **Explanation:** The code does not seem to implement any explicit measures against XSS or input sanitization, which can expose vulnerabilities if not addressed. Although the component mostly deals with internal service calls, ensuring that user inputs (like `searchText`) are sanitized before usage is crucial.
- **Improvement Suggestion:** Sanitize input values from users to prevent potential XSS vulnerabilities when rendering them in the template.

**Code Consistency and Style**
- **Score: 8/10**
- **Explanation:** The code follows Angular and TypeScript conventions well, with consistent naming and indentation. However, there are minor inconsistencies in the comments and the use of types (e.g., unnecessary type assertion in some locations).
- **Improvement Suggestion:** Remove redundant type assertions where TypeScript can infer types and improve comment clarity to maintain consistency across methods.

**Scalability and Extensibility**
- **Score: 7/10**
- **Explanation:** There is a fair amount of flexibility, but the reliance on certain hardcoded values (like certain IDs and rates) may limit scalability. The business logic for handling product quantities and pricing appears tightly coupled.
- **Improvement Suggestion:** Parameterize constants and magic numbers or use external configuration where applicable to increase extensibility for future changes.

**Error Handling and Robustness**
- **Score: 7/10**
- **Explanation:** The component has some basic mechanisms for handling errors (like opening a modal for insufficient inventory), but overall error handling is inconsistent. For example, the subscriber patterns are not adequately managed.
- **Improvement Suggestion:** Formalize error handling approaches across async methods and improve subscription management, perhaps using built-in error handling capabilities in RxJS.

### Overall Score: 7.43/10

### Code Improvement Summary:
1. **Error Handling:** Implement `try-catch` blocks around async calls to handle potential errors gracefully.
2. **Function Modularization:** Break down large functions into smaller helper functions for better readability and maintenance.
3. **Parallel Requests:** Utilize `forkJoin` to execute independent HTTP requests in parallel to enhance performance.
4. **Input Sanitization:** Ensure user inputs are sanitized to prevent XSS vulnerabilities.
5. **Parameterization of Constants:** Use configuration files or services to handle constants instead of hardcoding values directly in the code.

This comprehensive review reflects the strengths and weaknesses identified in the provided Angular component code and offers actionable suggestions for improvement, contributing to a more robust and maintainable implementation.[0m
==================================================
